"""
Demo - Handoff Summary From a Real Diff (Optional)
Day 1 - Session 1, Topic 3

Goal: Turn a real Git diff into the written summary line of a handoff artifact,
using a real LLM via API key (if provided), falling back to a small local model.

Everything structural in a handoff can be measured: the commit, the changed
files, the test result. The one field that needs prose is the summary a
reviewer reads first. This demo produces that field from the actual diff text.
A small local model, `google/flan-t5-base`, generates it when `transformers`
and the cached model are present; otherwise the demo falls back to a
deterministic summary built from the parsed diff and says so plainly.

This is the optional demo of the set. Skip it when class time is short: the
handoff structure is already demonstrated by demo-two-session-orchestration.py.

If an API key is set via .env (e.g. ANTHROPIC_API_KEY), it uses
the cloud model. Otherwise, it safely falls back. First run with the local
model downloads about 1 GB.

Run: python3 day1/demos/demo-handoff-summary.py
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_support import (  # noqa: E402
    assert_true,
    colab_note,
    git,
    heading,
    run_tests,
    sandbox,
    show_evidence,
)

MODEL_NAME = "google/flan-t5-base"
TARGET = Path("channels") / "email.py"
EDIT = ("your order shipped", "your order has shipped")
FOCUSED_TEST = "tests.test_email"



def load_api_model():
    """Return a generate() callable using litellm if configured, else None."""
    try:
        from llm_client import get_completion, PROVIDER
        import os
        if not any(os.getenv(k) for k in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "AZURE_API_KEY", "AZURE_AD_TOKEN"]):
            return None, None
            
        def generate(prompt):
            return get_completion([{"role": "user", "content": prompt}], tier="mini", max_tokens=100)
        
        return generate, f"{PROVIDER} API (mini tier)"
    except Exception:
        return None, None


def load_local_model():
    """Return a generate() callable, or None when the model is unavailable.

    The demo must never fail because a model is missing, so every failure mode
    here degrades to the deterministic path instead of raising.
    """
    try:
        import warnings

        warnings.filterwarnings("ignore")
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    except ImportError:
        print("  transformers is not installed; using the deterministic summary.")
        return None

    try:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME, local_files_only=True)
    except Exception:
        print(f"  {MODEL_NAME} is not in the local cache; using the deterministic summary.")
        print("  To enable it once, offline: python3 -c \"from transformers import "
              "AutoModelForSeq2SeqLM, AutoTokenizer; "
              f"AutoTokenizer.from_pretrained('{MODEL_NAME}'); "
              f"AutoModelForSeq2SeqLM.from_pretrained('{MODEL_NAME}')\"")
        return None

    model.eval()

    def generate(prompt):
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        output = model.generate(**inputs, max_new_tokens=48)  # greedy, deterministic
        return tokenizer.decode(output[0], skip_special_tokens=True).strip()

    return generate


def parse_diff(diff_text):
    """Extract the concrete facts a reviewer needs from the real diff."""
    added = [line[1:].strip() for line in diff_text.splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    removed = [line[1:].strip() for line in diff_text.splitlines()
               if line.startswith("-") and not line.startswith("---")]
    return added, removed


def deterministic_summary(files, added, removed):
    """Build a reviewable summary from parsed diff facts alone."""
    return (
        f"Changed {', '.join(files)}: {len(added)} line(s) added, "
        f"{len(removed)} removed, altering the rendered shipment wording."
    )


def looks_like_diff_echo(text, diff_text):
    """True when the model parroted diff metadata instead of summarizing.

    A small model often echoes its input. The handoff must not carry that, so
    the caller falls back to the deterministic summary when this triggers.
    """
    markers = ("diff --git", "index ", "@@", "+++", "---", "b/", "100644")
    return any(marker in text for marker in markers) or text[:20] in diff_text


def model_summary(generate, added, removed, files):
    """Ask the local model to describe only the changed lines.

    Raw diff text (headers, index lines, path markers) invites the model to
    echo metadata, so the prompt carries just the before and after code.
    """
    before = removed[0] if removed else "(nothing)"
    after = added[0] if added else "(nothing)"
    prompt = (
        "A developer edited a notification template.\n"
        f"Old text: {before}\n"
        f"New text: {after}\n"
        "Question: What kind of change is this? Answer in one sentence."
    )
    return generate(prompt)


def main():
    colab_note()
    heading("Local model availability")
    generate, source = load_api_model()
    if not generate:
        generate = load_local_model()
        source = MODEL_NAME if generate else "deterministic fallback"
    show_evidence("summary source", source)

    with sandbox() as (root, base):
        heading("Produce a real commit to summarize")
        path = root / TARGET
        path.write_text(path.read_text().replace(*EDIT))
        passed, _ = run_tests(FOCUSED_TEST, root)
        git("commit", "-q", "-am", "Refine shipment email wording", cwd=root)
        commit = git("rev-parse", "--short", "HEAD", cwd=root)
        changed = git("diff", "--name-only", f"{base}..{commit}", cwd=root).splitlines()
        diff_text = git("diff", f"{base}..{commit}", "--unified=0", cwd=root)

        show_evidence("commit", commit)
        show_evidence("changed files", ", ".join(changed))
        show_evidence("focused test", "passed" if passed else "FAILED")

        heading("The real diff handed to the summarizer")
        for line in diff_text.splitlines():
            if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                print(f"  {line}")

        added, removed = parse_diff(diff_text)
        heading("Generated summary field")
        if generate:
            raw = model_summary(generate, added, removed, changed)
            show_evidence("model output", raw or "(empty)")
            rejected = (
                not raw
                or len(raw.split()) < 4
                or looks_like_diff_echo(raw, diff_text)
            )
            if rejected:
                summary = deterministic_summary(changed, added, removed)
                source_used = "deterministic fallback (model output rejected)"
                show_evidence("rejected because", "echoed input or too terse")
                show_evidence("using instead", summary)
            else:
                # The model contributes prose; the measured facts stay authoritative.
                summary = f"{raw.rstrip('.')}. {deterministic_summary(changed, added, removed)}"
                source_used = f"{MODEL_NAME} prose + measured diff facts"
        else:
            summary = deterministic_summary(changed, added, removed)
            source_used = "deterministic fallback"
            show_evidence("fallback output", summary)

        heading("Assembled handoff artifact")
        handoff = {
            "task_id": "email-renderer",
            "base_commit": base,
            "implementation_commit": commit,
            "changed_files": sorted(changed),
            "summary": summary,
            "summary_source": source_used,
            "verification": {
                "command": f"python3 -m unittest {FOCUSED_TEST}",
                "status": "passed" if passed else "failed",
            },
            "unresolved_risks": [],
        }
        written = root / "handoffs" / "email.json"
        written.write_text(json.dumps(handoff, indent=2) + "\n")
        print(json.dumps(handoff, indent=2))

        heading("Evidence checks")
        assert_true(diff_text.strip() != "", "the diff came from a real commit")
        assert_true(
            any(EDIT[1] in line for line in added),
            "the diff contains the actual wording change",
        )
        assert_true(len(summary.split()) >= 4, "the summary field is reviewable prose")
        assert_true(
            not looks_like_diff_echo(summary, diff_text),
            "the summary is prose, not echoed diff metadata",
        )
        assert_true(
            json.loads(written.read_text())["implementation_commit"] == commit,
            "the handoff on disk records the real commit",
        )

    print(
        "\nTakeaway: Measure the structural handoff fields from Git and tests,"
        "\nand generate only the prose summary, from the real diff."
    )


if __name__ == "__main__":
    main()
