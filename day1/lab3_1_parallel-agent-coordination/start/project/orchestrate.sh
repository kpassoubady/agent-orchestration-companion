#!/bin/bash

# Trick of the Trade: Automated Handoff Orchestrator
# This script reads the handoff files from Agent 1 and Agent 2, extracts the
# implementation commits, and merges them into the main branch automatically
# using `jq`. It then runs the CI/CD integration gate automatically.

set -e

echo "Starting Automated Orchestration..."

run_check() {
    case "$1" in
        "python3 -m unittest tests.test_email tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html")
            python3 -m unittest tests.test_email tests.test_security.ChannelSecurityTest.test_email_escapes_untrusted_html
            ;;
        "python3 -m unittest tests.test_sms tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace")
            python3 -m unittest tests.test_sms tests.test_security.ChannelSecurityTest.test_sms_normalizes_control_whitespace
            ;;
        *)
            echo "Error: Unsupported verification command in handoff."
            exit 1
            ;;
    esac
}

# Ensure we are on main
git checkout main > /dev/null 2>&1

echo "1. Checking Email Agent Handoff..."
if [ ! -f "handoffs/email.json" ]; then
    echo "Error: handoffs/email.json not found."
    exit 1
fi

EMAIL_COMMIT=$(jq -er '.implementation_commit | select(type == "string" and test("^[0-9a-f]{40}$"))' handoffs/email.json)
EMAIL_CHECK=$(jq -er '.verification.command | strings' handoffs/email.json)

echo "   Merging Email Agent commit ($EMAIL_COMMIT)..."
git merge --no-edit "$EMAIL_COMMIT" > /dev/null 2>&1

echo "   Running Integration Gate (Email)..."
run_check "$EMAIL_CHECK"

echo "2. Checking SMS Agent Handoff..."
if [ ! -f "handoffs/sms.json" ]; then
    echo "Error: handoffs/sms.json not found."
    exit 1
fi

SMS_COMMIT=$(jq -er '.implementation_commit | select(type == "string" and test("^[0-9a-f]{40}$"))' handoffs/sms.json)
SMS_CHECK=$(jq -er '.verification.command | strings' handoffs/sms.json)

printf "Review both handoffs, changed-file boundaries, focused results, and the unchanged schema.\n"
read -r -p "Type 'yes' to approve the SMS merge: " APPROVAL
if [ "$APPROVAL" != "yes" ]; then
    echo "Approval not granted; stopping before the SMS merge."
    exit 1
fi

echo "   Merging SMS Agent commit ($SMS_COMMIT)..."
git merge --no-edit "$SMS_COMMIT" > /dev/null 2>&1

echo "   Running Integration Gate (SMS)..."
run_check "$SMS_CHECK"

echo "3. Running Full Combined Integration Gate..."
python3 -m unittest
python3 -m unittest tests.test_security

echo "✅ Orchestration complete! Commits merged and verified."
