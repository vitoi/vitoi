import json
import os
import subprocess
from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import Optional

try:
    import openai
except ImportError:  # pragma: no cover - openai may not be installed
    openai = None


def _call_openai(prompt: str, api_key: str) -> str:
    if openai is None:
        raise RuntimeError("openai package is required to call the API")
    openai.api_key = api_key
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    return resp["choices"][0]["message"]["content"].strip()


@dataclass
class SMTPSettings:
    host: str
    port: int = 25
    user: Optional[str] = None
    password: Optional[str] = None
    from_addr: Optional[str] = None
    to_addr: Optional[str] = None


class TestAgent:
    """Simple testing agent using OpenAI to generate and run tests."""

    def __init__(self, api_key: str, smtp: Optional[SMTPSettings] = None):
        self.api_key = api_key
        self.smtp = smtp

    def analyze_requirements(self, text: str) -> str:
        prompt = (
            "你是一名软件测试专家。请根据以下需求列出关键测试点并给出测试计划:\n" + text
        )
        return _call_openai(prompt, self.api_key)

    def generate_test_script(
        self, plan: str, script_path: str = "test_generated.py"
    ) -> str:
        prompt = "根据以下测试计划，为 pytest 生成完整的测试脚本:\n" + plan
        code = _call_openai(prompt, self.api_key)
        with open(script_path, "w", encoding="utf-8") as fh:
            fh.write(code)
        return script_path

    def run_tests(self, script_path: str) -> dict:
        subprocess.run(["pytest", script_path, "-q", "--json-report"], check=False)
        report_path = ".report.json"
        if os.path.exists(report_path):
            with open(report_path, encoding="utf-8") as fh:
                return json.load(fh)
        return {}

    def summarize(self, report: dict) -> str:
        prompt = (
            "以下是 pytest 生成的 JSON 报告，请给出测试总结并指出失败原因:\n"
            + json.dumps(report)
        )
        return _call_openai(prompt, self.api_key)

    def send_report(self, summary: str) -> None:
        if not self.smtp or not self.smtp.to_addr:
            print(summary)
            return
        import smtplib

        msg = MIMEText(summary, "plain", "utf-8")
        msg["Subject"] = "自动化测试报告"
        from_addr = self.smtp.from_addr or self.smtp.user
        msg["From"] = from_addr
        msg["To"] = self.smtp.to_addr
        with smtplib.SMTP(self.smtp.host, self.smtp.port) as server:
            if self.smtp.user and self.smtp.password:
                server.login(self.smtp.user, self.smtp.password)
            server.sendmail(from_addr, [self.smtp.to_addr], msg.as_string())
