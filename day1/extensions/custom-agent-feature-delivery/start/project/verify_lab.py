import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
AGENTS = {
    "story-planner.md": {"name": "story-planner", "tools": {"Read", "Glob", "Grep"}, "model": "haiku"},
    "feature-implementer.md": {
        "name": "feature-implementer",
        "tools": {"Read", "Glob", "Grep", "Edit", "Bash"},
        "model": "sonnet",
    },
    "acceptance-reviewer.md": {
        "name": "acceptance-reviewer",
        "tools": {"Read", "Glob", "Grep", "Bash"},
        "model": "sonnet",
    },
}
ALLOWED_CHANGES = {
    ".claude/agents/story-planner.md",
    ".claude/agents/feature-implementer.md",
    ".claude/agents/acceptance-reviewer.md",
    "preferences.py",
    "router.py",
}


def run(*args):
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True)


def frontmatter(path):
    text = path.read_text()
    parts = text.split("---", 2)
    if len(parts) != 3:
        return {}, ""
    fields = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip()
    return fields, parts[2].strip()


def verify_agents(errors):
    for filename, expected in AGENTS.items():
        path = ROOT / ".claude" / "agents" / filename
        if not path.exists():
            errors.append(f"Missing project agent: {path.relative_to(ROOT)}")
            continue
        fields, body = frontmatter(path)
        tools = {tool.strip() for tool in fields.get("tools", "").split(",") if tool.strip()}
        if fields.get("name") != expected["name"]:
            errors.append(f"{filename} has the wrong name")
        if not fields.get("description"):
            errors.append(f"{filename} needs a delegation description")
        if tools != expected["tools"]:
            errors.append(f"{filename} tools must be {sorted(expected['tools'])}")
        if fields.get("model") != expected["model"]:
            errors.append(f"{filename} must use model {expected['model']}")
        if len(body.split()) < 15:
            errors.append(f"{filename} needs a specific operating prompt")


def verify_git_boundaries(errors):
    if run("git", "rev-parse", "--verify", "lab-base").returncode != 0:
        return
    changed = run("git", "diff", "--name-only", "lab-base")
    if changed.returncode != 0:
        errors.append("Could not inspect changes from lab-base")
        return
    untracked = run("git", "ls-files", "--others", "--exclude-standard")
    changed_files = set(changed.stdout.split()) | set(untracked.stdout.split())
    missing = ALLOWED_CHANGES - changed_files
    unexpected = changed_files - ALLOWED_CHANGES
    if missing:
        errors.append(f"Required lab changes are missing: {', '.join(sorted(missing))}")
    if unexpected:
        errors.append(f"Files outside lab ownership changed: {', '.join(sorted(unexpected))}")
    if run("git", "diff", "--quiet", "lab-base", "--", "tests").returncode != 0:
        errors.append("Acceptance tests changed from lab-base")


def main():
    errors = []
    verify_agents(errors)
    verify_git_boundaries(errors)
    tests = run(sys.executable, "-m", "unittest")
    if tests.returncode != 0:
        errors.append("Full acceptance suite failed")
    if errors:
        print("CUSTOM AGENT LAB INVALID")
        for error in errors:
            print(f"- {error}")
        if tests.stdout or tests.stderr:
            print(tests.stdout + tests.stderr)
        raise SystemExit(1)
    print("CUSTOM AGENT LAB VALID")
    print("Agents: story-planner -> feature-implementer -> acceptance-reviewer")
    print("Owned implementation: preferences.py, router.py")
    print("Full acceptance suite: passed")


if __name__ == "__main__":
    main()
