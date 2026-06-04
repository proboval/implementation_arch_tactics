# pc/app/ai/ai_event_controller.py
import time
from datetime import datetime
from typing import Optional, Dict, Any

from .ai_store import AiRuntime, EventStore
from .motion_trigger import MotionTrigger
from .vision_client import client_signature, create_vision_client, resolve_provider_settings


def _now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe_bool(x) -> bool:
    return bool(x) if isinstance(x, bool) else (str(x).lower() in ("1", "true", "yes", "on"))


def _clamp_int(x, lo, hi, default):
    try:
        v = int(x)
        return max(lo, min(hi, v))
    except Exception:
        return default


def _clamp_float(x, lo, hi, default):
    try:
        v = float(x)
        return max(lo, min(hi, v))
    except Exception:
        return default


def _should_call(now: float, last_ts: float, interval: float) -> bool:
    return (now - last_ts) >= interval


class AIEventController:
    """Encapsulates AI state machine logic, event lifecycle, and config-driven behavior."""

    def __init__(
        self,
        ai_rt: AiRuntime,
        event_store: EventStore,
        motion_trigger: Optional[MotionTrigger] = None,
        logger=None,
    ):
        self.ai_rt = ai_rt
        self.event_store = event_store
        self.logger = logger
        self._motion = motion_trigger or MotionTrigger()
        self._client = None
        self._last_client_sig: Optional[str] = None

    def process_state(self, cfg: Dict[str, Any], frame) -> None:
        """Process current AI state (SLEEP or OBSERVE) based on config and frame."""
        ai_enabled = _safe_bool(cfg.get("ai_enabled", False))
        ai_mode = str(cfg.get("ai_mode", "triggered"))

        if not ai_enabled or ai_mode != "triggered":
            return

        observe_interval = _clamp_float(cfg.get("ai_interval_observe", 5), 1, 60, 5)
        dwell_threshold = _clamp_float(cfg.get("ai_dwell_threshold_sec", 5), 1, 600, 5)
        end_grace = _clamp_float(cfg.get("ai_end_grace_sec", 3), 0, 60, 3)

        # Update motion trigger parameters
        self._motion.ratio_threshold = _clamp_float(
            cfg.get("motion_ratio_threshold", 0.02), 0.001, 0.5, 0.02
        )
        self._motion.min_trigger_interval_sec = _clamp_float(
            cfg.get("motion_min_interval", 1.0), 0.1, 10.0, 1.0
        )

        settings = resolve_provider_settings(cfg)
        if not settings["model"] or not settings["api_key"]:
            missing = []
            if not settings["model"]:
                missing.append("model")
            if not settings["api_key"]:
                missing.append("api_key")
            with self.ai_rt.lock:
                self.ai_rt.last_ai_error = f"AI config missing: {', '.join(missing)}"
            return

        # Initialize / rebuild client if config changed
        sig = client_signature(cfg)
        if self._client is None or sig != self._last_client_sig:
            self._rebuild_client(cfg, settings)
            if self._client is None:
                return

        now = time.time()
        with self.ai_rt.lock:
            state = self.ai_rt.state

        if state == "SLEEP":
            self._handle_sleep_state(now, cfg, frame, observe_interval)
        elif state == "OBSERVE":
            self._handle_observe_state(now, cfg, frame, observe_interval, dwell_threshold, end_grace)

    def _rebuild_client(self, cfg: Dict[str, Any], settings: Dict[str, Any]) -> None:
        try:
            self._client = create_vision_client(cfg)
            self._last_client_sig = client_signature(cfg)
            with self.ai_rt.lock:
                self.ai_rt.last_ai_error = ""
            if self.logger:
                self.logger.info(
                    f"Vision client ready: provider={settings['provider']} model={settings['model']}"
                )
        except Exception as e:
            with self.ai_rt.lock:
                self.ai_rt.last_ai_error = f"Vision client init failed: {e}"
            if self.logger:
                self.logger.error(f"Vision client init failed: {e}")
            self._client = None

    def _handle_sleep_state(self, now: float, cfg: Dict[str, Any], frame, observe_interval: float) -> None:
        triggered, ratio = self._motion.check(frame)
        if triggered:
            with self.ai_rt.lock:
                self.ai_rt.state = "OBSERVE"
                self.ai_rt.last_trigger_ts = now
                self.ai_rt.last_trigger_reason = f"motion_ratio={ratio:.4f}"
                self.ai_rt.event_id = f"evt_{int(now)}"
                self.ai_rt.event_start_ts = now
                self.ai_rt.person_present_acc_sec = 0.0
                self.ai_rt.last_person_true_ts = None
                self.ai_rt.last_person_false_ts = None
                self.ai_rt.dwell_confirmed = False
                self.ai_rt.last_ai_error = ""
                self.ai_rt.last_ai_json = None

            self.event_store.add_event({
                "event_id": self.ai_rt.event_id,
                "kind": "event_start",
                "trigger": "motion",
                "motion_ratio": ratio,
                "time_text": _now_text(),
            })
            if self.logger:
                self.logger.info(f"AI event_start (motion ratio={ratio:.4f})")

    def _handle_observe_state(
        self,
        now: float,
        cfg: Dict[str, Any],
        frame,
        observe_interval: float,
        dwell_threshold: float,
        end_grace: float,
    ) -> None:
        with self.ai_rt.lock:
            last_call = self.ai_rt.last_ai_call_ts
            event_id = self.ai_rt.event_id
            event_start_ts = self.ai_rt.event_start_ts or now
            person_acc = self.ai_rt.person_present_acc_sec
            last_true = self.ai_rt.last_person_true_ts
            last_false = self.ai_rt.last_person_false_ts
            dwell_ok = self.ai_rt.dwell_confirmed

        if not _should_call(now, last_call, observe_interval):
            return

        prompt_template = str(cfg.get("ai_prompt_template", "") or "")
        scene_profile = str(cfg.get("ai_scene_profile", "") or "")
        session_focus = str(cfg.get("ai_session_focus", "") or "")
        extra_prompt = str(cfg.get("ai_prompt_extra", "") or "")
        jpeg_quality = _clamp_int(cfg.get("ai_jpeg_quality", 85), 50, 95, 85)

        try:
            parsed = self._client.analyze_frame(
                frame,
                time_text=_now_text(),
                prompt_template=prompt_template,
                scene_profile=scene_profile,
                session_focus=session_focus,
                extra_prompt=extra_prompt,
                jpeg_quality=jpeg_quality,
            )
            has_person = bool(parsed.get("has_person", False))
            confidence = float(parsed.get("confidence", 0.0) or 0.0)

            with self.ai_rt.lock:
                self.ai_rt.last_ai_call_ts = now
                self.ai_rt.last_ai_json = parsed
                self.ai_rt.last_ai_error = ""

            self.event_store.add_event({
                "event_id": event_id,
                "kind": "ai_frame",
                "time_text": _now_text(),
                "has_person": has_person,
                "confidence": confidence,
                "ai": parsed,
            })

        except Exception as e:
            with self.ai_rt.lock:
                self.ai_rt.last_ai_call_ts = now
                self.ai_rt.last_ai_error = str(e)

            self.event_store.add_event({
                "event_id": event_id,
                "kind": "ai_error",
                "time_text": _now_text(),
                "error": str(e),
            })
            if self.logger:
                self.logger.error(f"AI analyze error: {e}")
            return

        # Dwell integration
        if has_person:
            person_acc += observe_interval
            last_true = now
            last_false = None
        else:
            last_false = now if last_false is None else last_false

        # Dwell confirmed
        if (not dwell_ok) and person_acc >= dwell_threshold:
            dwell_ok = True
            self.event_store.add_event({
                "event_id": event_id,
                "kind": "dwell_confirmed",
                "time_text": _now_text(),
                "dwell_sec": round(person_acc, 2),
                "threshold_sec": dwell_threshold,
            })
            if self.logger:
                self.logger.info(f"dwell_confirmed: {person_acc:.2f}s >= {dwell_threshold}s")

        # End condition
        ended = False
        if last_false is not None and (now - last_false) >= end_grace:
            ended = True

        with self.ai_rt.lock:
            self.ai_rt.person_present_acc_sec = person_acc
            self.ai_rt.last_person_true_ts = last_true
            self.ai_rt.last_person_false_ts = last_false
            self.ai_rt.dwell_confirmed = dwell_ok

        if ended:
            self.event_store.add_event({
                "event_id": event_id,
                "kind": "event_end",
                "time_text": _now_text(),
                "total_event_sec": round(now - event_start_ts, 2),
                "person_present_acc_sec": round(person_acc, 2),
                "dwell_confirmed": dwell_ok,
            })
            if self.logger:
                self.logger.info(f"AI event_end: event_id={event_id}")

            with self.ai_rt.lock:
                self.ai_rt.state = "SLEEP"
                self.ai_rt.event_id = None
                self.ai_rt.event_start_ts = None
                self.ai_rt.person_present_acc_sec = 0.0
                self.ai_rt.last_person_true_ts = None
                self.ai_rt.last_person_false_ts = None
                self.ai_rt.dwell_confirmed = False
