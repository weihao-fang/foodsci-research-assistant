"""Run explicit CSV analysis tasks, stopping on error; no background jobs or networking."""
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path


def run_workflow(config_path, output_dir):
    config_path, output_dir = Path(config_path).resolve(), Path(output_dir).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    if not isinstance(config, dict):
        raise ValueError("Config must be a JSON object")
    tasks = config.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Config requires a nonempty tasks list")
    commands, identifiers = [], set()
    for task in tasks:
        if not isinstance(task, dict) or not isinstance(task.get("id"), str):
            raise ValueError("Each task needs a string id")
        task_id, mode = task["id"], task.get("mode")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", task_id) or task_id in identifiers:
            raise ValueError("Task ids must be unique lowercase kebab-case")
        if task_id == "run-report":
            raise ValueError("Task id run-report is reserved for the workflow report")
        identifiers.add(task_id)
        if mode not in ("raw", "digestion", "doi") or not isinstance(task.get("input"), str):
            raise ValueError("Each task needs mode raw/digestion/doi and an input path")
        source = (config_path.parent / task["input"]).resolve()
        if not source.is_file():
            raise ValueError(f"Input not found: {source}")
        target = output_dir / f"{task_id}.json"
        script_dir = Path(__file__).resolve().parent
        command = [sys.executable, "-X", "utf8", "-B",
                   str(script_dir / ("verify_doi.py" if mode == "doi" else "analyze.py"))]
        if mode != "doi":
            command.append(mode)
        command += ["--input", str(source), "--output", str(target)]
        if mode == "raw":
            if not isinstance(task.get("reference_group"), str) or not task["reference_group"].strip():
                raise ValueError("RAW task requires reference_group")
            command += ["--reference-group", task["reference_group"]]
        commands.append((task_id, mode, command))
    output_dir.mkdir(parents=True, exist_ok=False)
    report = {"status": "completed", "network": "disabled", "needs_review": False, "tasks": []}
    for task_id, mode, command in commands:
        child_env = dict(os.environ, PYTHONIOENCODING="utf-8")
        completed = subprocess.run(command, capture_output=True, text=True, encoding="utf-8", env=child_env)
        review = mode == "doi" and completed.returncode == 1 and (output_dir / f"{task_id}.json").is_file()
        success = completed.returncode == 0 or review
        report["tasks"].append({"id": task_id, "exit_code": completed.returncode,
                                "status": "needs_review" if review else ("completed" if success else "failed"),
                                "stderr": completed.stderr.strip(),
                                "output": f"{task_id}.json" if success else None})
        report["needs_review"] = report["needs_review"] or review
        if not success:
            report["status"] = "failed"
            break
    report["not_run"] = [task_id for task_id, _, _ in commands[len(report["tasks"]):]]
    (output_dir / "run-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    try:
        report = run_workflow(args.config, args.output_dir)
    except (ValueError, OSError, TypeError) as error:
        parser.exit(2, f"Workflow failed: {error}\n")
    print(json.dumps(report, ensure_ascii=True))
    return 0 if report["status"] == "completed" else 2


if __name__ == "__main__":
    sys.exit(main())
