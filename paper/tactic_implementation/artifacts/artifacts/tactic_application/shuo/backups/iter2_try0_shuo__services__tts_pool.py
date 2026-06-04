"""
ElevenLabs TTS connection pool.

Manages a cache of warm TTS connections, dispatching ready instances.
Connection lifecycle (start/cancel) is now delegated to TTSService itself.

Usage:
    pool = TTSPool(pool_size=1)
    await pool.start()

    tts = await pool.get(on_audio=..., on_done=...)
    # tts is ready to use immediately (if warm) or after a fresh connect

    await pool.stop()
"""

import asyncio
from typing import Optional, Callable, Awaitable, List
from dataclasses import dataclass

from .tts import TTSService
from ..log import ServiceLogger

log = ServiceLogger("TTSPool")


@dataclass
class _Entry:
    """A pooled TTS connection with its creation timestamp."""
    tts: TTSService
    created_at: float  # time.monotonic()


class TTSPool:
    """
    Connection pool for ElevenLabs TTS WebSockets.

    - Maintains `pool_size` warm connections in the background
    - Dispenses warm connections via get() with callback rebinding
    - Delegates warm-up and eviction to TTSService internal state machine
    """

    def __init__(self, pool_size: int = 1):
        self._pool_size = pool_size

        self._ready: List[_Entry] = []
        self._running = False
        self._fill_event = asyncio.Event()
        self._fill_task: Optional[asyncio.Task] = None

    @property
    def available(self) -> int:
        """Number of warm connections ready to dispense."""
        return len(self._ready)

    async def start(self) -> None:
        """Start the pool and begin warming connections."""
        if self._running:
            return

        self._running = True
        self._fill_task = asyncio.create_task(self._fill_loop())

    async def get(
        self,
        on_audio: Callable[[str], Awaitable[None]],
        on_done: Callable[[], Awaitable[None]],
    ) -> TTSService:
        """
        Get a connected TTS service with the given callbacks.

        Returns a warm connection if available, otherwise triggers warm-up
        and blocks until one is ready.
        """
        # Try to grab a warm connection
        while self._ready:
            entry = self._ready.pop(0)
            if entry.tts.is_warm:
                entry.tts.bind(on_audio, on_done)
                log.info("Dispensed warm connection")
                self._trigger_fill()
                return entry.tts
            else:
                # Connection is no longer warm; discard and retry
                log.info("Discarded non-warm connection")

        # No warm connections available -- create fresh (blocking)
        log.info("Pool empty, connecting fresh...")
        tts = TTSService(on_audio=on_audio, on_done=on_done)
        await tts.warm()
        self._trigger_fill()
        return tts

    async def stop(self) -> None:
        """Shut down pool and clean up all connections."""
        self._running = False
        self._fill_event.set()  # unblock fill loop

        if self._fill_task:
            self._fill_task.cancel()
            try:
                await self._fill_task
            except asyncio.CancelledError:
                pass
            self._fill_task = None

        for entry in self._ready:
            await entry.tts.cancel()
        self._ready.clear()

    def _trigger_fill(self) -> None:
        """Signal the fill loop to check pool levels."""
        self._fill_event.set()

    async def _fill_loop(self) -> None:
        """Background loop that keeps the pool at target size."""
        try:
            while self._running:
                # Fill to target
                while self._running and len(self._ready) < self._pool_size:
                    tts = TTSService(on_audio=lambda _: None, on_done=lambda: None)
                    try:
                        await tts.warm()
                        self._ready.append(
                            _Entry(tts=tts, created_at=time.monotonic())
                        )
                        log.info(
                            f"🔥 Warm connection ready "
                            f"({len(self._ready)}/{self._pool_size})"
                        )
                    except Exception as e:
                        log.error("Pre-connect failed", e)
                        await tts.cancel()
                        await asyncio.sleep(1.0)  # back off

                # Wait for signal (dispensed) or periodic refresh
                self._fill_event.clear()
                try:
                    await asyncio.wait_for(
                        self._fill_event.wait(),
                        timeout=5.0,
                    )
                except asyncio.TimeoutError:
                    pass  # periodic check

        except asyncio.CancelledError:
            pass


# Import time for _Entry.created_at usage
import time
