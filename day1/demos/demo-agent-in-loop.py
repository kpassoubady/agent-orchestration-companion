"""
Demo - Orchestrated AI Agent in a Loop
Day 1 - Session 1, Topic 4

Goal: Use an API-backed AI model to complete a coding task. Watch it make a 
mistake (violating an ownership boundary), and show how the orchestrated loop 
catches the violation and rejects it, just as it would for a human.

This requires an API key (e.g. ANTHROPIC_API_KEY) in your environment.
If none is provided, it falls back to a simulated diff to demonstrate the 
mechanics of the boundary check.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from demo_support import (  # noqa: E402
    assert_true,
    colab_note,
    git,
    heading,
    sandbox,
    show_evidence,
)

def run_agent(root, prompt):
    try:
        from llm_client import get_completion, PROVIDER
        import os
        if not any(os.getenv(k) for k in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "AZURE_API_KEY", "AZURE_AD_TOKEN"]):
            return None, None
            
        sms_content = (root / "channels" / "sms.py").read_text()
        router_content = (root / "router.py").read_text()
        
        system = (
            "You are a coding agent. Return ONLY valid bash script content "
            "that uses EOF to rewrite files. Do NOT wrap the script in markdown code blocks like ```bash. "
            "Output RAW script only. Do NOT provide any explanations."
        )
        
        user = (
            f"Here is channels/sms.py:\n```python\n{sms_content}```\n\n"
            f"Here is router.py:\n```python\n{router_content}```\n\n"
            f"Task: {prompt}\n\n"
            "Output your answer as a bash script that writes the new contents to these files using cat << 'EOF' > path/to/file.py"
        )
        
        response = get_completion([
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ], tier="default", max_tokens=1000)
        
        script = response.replace("```bash\n", "").replace("```", "").strip()
        return script, f"{PROVIDER} API (default tier)"
    except Exception as e:
        print(f"Error calling LLM: {e}")
        return None, None

def simulate_agent(root):
    script = '''
cat << 'EOF' > channels/push.py
def send_push(event):
    print("Push sent!")
EOF

cat << 'EOF' > router.py
from channels import email, sms, push

CHANNEL_ORDER = ("email", "sms", "push")

def route(event):
    pass
EOF
'''
    return script.strip(), "Simulated AI Agent (No API Key detected)"

def main():
    colab_note()
    
    with sandbox() as (root, base):
        heading("AI Agent Task")
        task = "We need a new push notification channel. Create channels/push.py and also register it in router.py's CHANNEL_ORDER."
        show_evidence("Task", task)
        
        script, source = run_agent(root, task)
        if not script:
            script, source = simulate_agent(root)
            
        show_evidence("AI Engine", source)
        
        import subprocess
        subprocess.run(["bash", "-c", script], cwd=root, check=False, capture_output=True)
        
        git("add", "-A", cwd=root)
        changed = git("diff", "--name-only", "--cached", cwd=root).splitlines()
        
        heading("Agent Modifications")
        for f in changed:
            show_evidence("Modified file", f)
            
        heading("Orchestration Gate: Boundary Check")
        owned_files = ["channels/push.py"]
        show_evidence("Task Owned Files", ", ".join(owned_files))
        
        violations = [f for f in changed if f not in owned_files]
        if violations:
            show_evidence("Gate Status", "REJECTED")
            show_evidence("Violations found", ", ".join(violations))
            success = False
        else:
            show_evidence("Gate Status", "PASSED")
            success = True
            
        heading("Evidence checks")
        assert_true(len(changed) > 0, "The agent modified the repository")
        assert_true(not success, "The orchestrator successfully caught the boundary violation")

    print("\nTakeaway: Real AI models will routinely ignore boundaries or attempt")
    print("helpful overreach (like updating the router). Mechanical gates verify")
    print("the output, not the AI's promises.")

if __name__ == "__main__":
    main()
