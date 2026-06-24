#!/usr/bin/env python3
"""
measure_edit_coverage.py — the missing instrument for §5.2 (RQ2/RQ3).

It answers the question the panel review said the paper only *infers*:
    Do a project's existing tests actually EXERCISE the code the LLM edited?
    And can the regression gate even fire (positive control)?

For each repository that the pipeline modified (pipeline_status == "applied"),
this script:
  1. clones the repo into a scratch dir,
  2. creates an isolated venv and best-effort installs the project + pytest +
     coverage,
  3. runs the test suite under coverage.py on the ORIGINAL (pre-edit) code,
  4. reports the line coverage of the files the LLM later modified
     (from the dataset's `common_files_changed` column), and
  5. (optional, --positive-control) injects a trivial behaviour-breaking
     mutation into the FIRST covered line of a modified file and re-runs the
     suite to confirm at least one test fails — i.e. that the gate CAN fire.

Output: coverage_results.csv with one row per repo:
    repo, status, has_tests, suite_ok, modified_files,
    modified_cov_pct, overall_cov_pct, positive_control_detected, note

Interpreting the result for the paper:
  * If modified_cov_pct is ~0 across repos -> the suites do not reach the
    edits, so "0 regressions" means *untested*, not *safe* (confirms the
    test-adequacy gap, turning the inferred claim in §5.2 into a measured one).
  * If positive_control_detected is True where coverage>0 -> the gate works;
    the null is meaningful, not a broken harness.

Usage:
    python3 measure_edit_coverage.py \
        --dataset ../../tactic_implementation/artifacts/improvement_maintainability_dataset.csv \
        --out coverage_results.csv [--limit N] [--positive-control] [--timeout 600]

Requirements on the host: git, python3 (>=3.9), network access. Each repo is
built in its own venv, so the host environment is not polluted. Repos that fail
to clone/install/collect are recorded (note=...) and skipped, exactly as the
main pipeline treats such failures.
"""
import argparse, csv, json, os, re, shutil, subprocess, sys, tempfile, venv
from pathlib import Path


def run(cmd, cwd=None, timeout=600, env=None):
    try:
        p = subprocess.run(cmd, cwd=cwd, env=env, timeout=timeout,
                           capture_output=True, text=True)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"
    except Exception as e:  # noqa
        return 1, "", str(e)


def modified_files(cell):
    """Parse 'app.py:69.3->73.7; tools.py:...' -> ['app.py','tools.py']."""
    out = []
    for part in (cell or "").split(";"):
        f = part.split(":")[0].strip()
        if f.endswith(".py"):
            out.append(f)
    return out


def has_test_infra(repo):
    if any((repo / m).exists() for m in ("pytest.ini", "pyproject.toml",
                                         "setup.cfg", "tox.ini")):
        # presence of config doesn't guarantee tests; also look for test files
        pass
    for p in repo.rglob("*.py"):
        n = p.name.lower()
        if n.startswith("test_") or n.endswith("_test.py") or "tests" in p.parts:
            return True
    return False


def make_venv(path):
    venv.EnvBuilder(with_pip=True).create(path)
    bindir = "Scripts" if os.name == "nt" else "bin"
    return str(Path(path) / bindir / "python")


def install(py, repo, timeout):
    run([py, "-m", "pip", "install", "-q", "-U", "pip", "coverage", "pytest"],
        timeout=timeout)
    # best-effort project deps
    for cmd in (["-m", "pip", "install", "-q", "-e", "."],
                ["-m", "pip", "install", "-q", "-r", "requirements.txt"]):
        if cmd[-1] == "." and not (repo / "pyproject.toml").exists() \
                and not (repo / "setup.py").exists():
            continue
        if cmd[-1] == "requirements.txt" and not (repo / "requirements.txt").exists():
            continue
        run([py] + cmd, cwd=str(repo), timeout=timeout)


def coverage_for(py, repo, mod_files, timeout):
    """Run pytest under coverage; return (suite_ok, overall_pct, mod_pct)."""
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    rc, out, err = run([py, "-m", "coverage", "run", "--source", ".",
                        "-m", "pytest", "-q", "--no-header"],
                       cwd=str(repo), timeout=timeout, env=env)
    suite_ok = rc in (0, 1)  # 0=all pass, 1=some fail; both mean tests ran
    if not (repo / ".coverage").exists():
        return suite_ok, None, None
    run([py, "-m", "coverage", "json", "-o", ".cov.json"], cwd=str(repo),
        timeout=120)
    cj = repo / ".cov.json"
    if not cj.exists():
        return suite_ok, None, None
    data = json.loads(cj.read_text())
    files = data.get("files", {})
    overall = data.get("totals", {}).get("percent_covered")
    # match modified files by basename against covered file keys
    tot = cov = 0
    for mf in mod_files:
        base = os.path.basename(mf)
        for k, v in files.items():
            if os.path.basename(k) == base:
                s = v.get("summary", {})
                tot += s.get("num_statements", 0)
                cov += s.get("covered_lines", 0)
    mod_pct = (100.0 * cov / tot) if tot else None
    return suite_ok, overall, mod_pct


def positive_control(py, repo, mod_files, timeout):
    """Mutate the first 'return'/'=' line of a modified file; expect a failure."""
    for mf in mod_files:
        f = repo / mf
        if not f.exists():
            continue
        lines = f.read_text(errors="ignore").splitlines()
        for i, ln in enumerate(lines):
            if re.match(r"\s*return\s+\S", ln):
                bak = lines[:]
                lines[i] = re.sub(r"return\s+.*", "return None  # PC-mutation", ln)
                f.write_text("\n".join(lines))
                rc, _, _ = run([py, "-m", "pytest", "-q", "--no-header"],
                               cwd=str(repo), timeout=timeout)
                f.write_text("\n".join(bak))  # restore
                return rc not in (0, 5)  # nonzero (excl. 5=no tests) => detected
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--out", default="coverage_results.csv")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--positive-control", action="store_true")
    a = ap.parse_args()

    rows = [r for r in csv.DictReader(open(a.dataset))
            if r.get("pipeline_status") == "applied"]
    if a.limit:
        rows = rows[:a.limit]
    print(f"{len(rows)} applied repositories to process", file=sys.stderr)

    out = []
    for i, r in enumerate(rows, 1):
        repo_name = r["repo_full_name"]
        url = r.get("clone_url") or f"https://github.com/{repo_name}.git"
        mods = modified_files(r.get("common_files_changed", ""))
        rec = {"repo": repo_name, "status": "", "has_tests": "",
               "suite_ok": "", "modified_files": ";".join(mods),
               "modified_cov_pct": "", "overall_cov_pct": "",
               "positive_control_detected": "", "note": ""}
        tmp = tempfile.mkdtemp(prefix="cov_")
        try:
            print(f"[{i}/{len(rows)}] {repo_name}", file=sys.stderr)
            rc, _, err = run(["git", "clone", "--depth", "1", url, tmp],
                             timeout=a.timeout)
            if rc != 0:
                rec["status"] = "clone_failed"; rec["note"] = err[:120]; continue
            repo = Path(tmp)
            rec["has_tests"] = has_test_infra(repo)
            if not rec["has_tests"]:
                rec["status"] = "no_tests"; continue
            py = make_venv(os.path.join(tmp, ".venv"))
            install(py, repo, a.timeout)
            suite_ok, overall, modpct = coverage_for(py, repo, mods, a.timeout)
            rec["status"] = "measured"
            rec["suite_ok"] = suite_ok
            rec["overall_cov_pct"] = "" if overall is None else round(overall, 1)
            rec["modified_cov_pct"] = "" if modpct is None else round(modpct, 1)
            if a.positive_control and mods:
                rec["positive_control_detected"] = positive_control(py, repo, mods, a.timeout)
        except Exception as e:  # noqa
            rec["status"] = "error"; rec["note"] = str(e)[:120]
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
            out.append(rec)

    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0].keys()))
        w.writeheader(); w.writerows(out)

    # summary
    meas = [r for r in out if r["status"] == "measured"]
    cov0 = [r for r in meas if r["modified_cov_pct"] in ("", 0, 0.0)]
    print(f"\nwrote {a.out}: {len(out)} repos, {len(meas)} measured, "
          f"{len(cov0)} with ~0% coverage of edited files", file=sys.stderr)


if __name__ == "__main__":
    main()
