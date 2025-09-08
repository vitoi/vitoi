#!/usr/bin/env python
"""Command line interface for the test agent."""
from test_agent.agent import TestAgent, SMTPSettings
import argparse

parser = argparse.ArgumentParser(description="Run the LLM-based test agent")
parser.add_argument("requirement", help="Requirement description text")
parser.add_argument("--api-key", dest="api_key", required=True, help="OpenAI API key")
parser.add_argument("--smtp-host", dest="smtp_host")
parser.add_argument("--smtp-to", dest="smtp_to")
parser.add_argument("--smtp-user", dest="smtp_user")
parser.add_argument("--smtp-password", dest="smtp_password")
args = parser.parse_args()

smtp = None
if args.smtp_host and args.smtp_to:
    smtp = SMTPSettings(
        host=args.smtp_host,
        to_addr=args.smtp_to,
        user=args.smtp_user,
        password=args.smtp_password,
    )

agent = TestAgent(api_key=args.api_key, smtp=smtp)
plan = agent.analyze_requirements(args.requirement)
script = agent.generate_test_script(plan)
report = agent.run_tests(script)
summary = agent.summarize(report)
agent.send_report(summary)
