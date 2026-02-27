# MIT License © 2025 Motohiro Suzuki
import json, yaml
from pathlib import Path

ROOT = Path(".")
RUNS = ROOT / "out/ci/actions_runs.json"
JOBS = ROOT / "out/ci/actions_jobs.json"
CLAIMS = ROOT / "claims/claims.yaml"
OUT = ROOT / "poc_report.md"

def load_json(p):
    return json.loads(p.read_text(encoding="utf-8"))

def main():
    runs = load_json(RUNS)
    jobs = load_json(JOBS)
    claims = yaml.safe_load(CLAIMS.read_text(encoding="utf-8"))

    repo = runs.get("repo")
    run_id = runs.get("run_id")
    run_url = f"https://github.com/{repo}/actions/runs/{run_id}"

    job_index = {j["name"]: j for j in jobs.get("jobs", [])}

    lines = []
    lines.append("# PoC Report (Stage202)")
    lines.append("")
    lines.append(f"- Repo: `{repo}`")
    lines.append(f"- Run ID: `{run_id}`")
    lines.append(f"- Run URL: {run_url}")
    lines.append("")
    lines.append("## Claim → required_jobs → CI job link")
    lines.append("")

    for claim, obj in claims.get("claims", claims).items():
        lines.append(f"### {claim}")
        rj = obj.get("required_jobs", [])
        ev = obj.get("evidence_paths", [])
        lines.append("- required_jobs:")
        for j in rj:
            if j in job_index:
                url = job_index[j].get("html_url")
                concl = job_index[j].get("conclusion")
                lines.append(f"  - [{j}]({url}) ({concl})")
            else:
                lines.append(f"  - {j} (not found)")
        lines.append("- evidence_paths:")
        for e in ev:
            lines.append(f"  - `{e}`")
        lines.append("")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print("[OK] wrote poc_report.md")

if __name__ == "__main__":
    main()
