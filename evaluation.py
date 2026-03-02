"""
Simple evaluation script for the Personal AI Coach prompt setup.

Runs three test cases against the plan prompt and coach styles; prints a short report.

Usage:
    export OPENAI_API_KEY=your_key_here
    python evaluation.py
"""

import os
from dataclasses import dataclass
from typing import List

from openai import OpenAI

from prompts import COACH_STYLE_DESCRIPTIONS, PLAN_SYSTEM_TEMPLATE


@dataclass
class TestCase:
    name: str
    goal: str
    constraints: str
    coach_style: str


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set; cannot run evaluation.")
    return OpenAI()


def run_test_case(client: OpenAI, test: TestCase, temperature: float = 0.3) -> str:
    system_content = PLAN_SYSTEM_TEMPLATE.format(
        coach_style=test.coach_style,
        style_guidance=COACH_STYLE_DESCRIPTIONS[test.coach_style],
    )
    user_parts = [f"**Goal:** {test.goal}"]
    if test.constraints:
        user_parts.append(f"**Constraints:** {test.constraints}")
    user_content = "\n\n".join(user_parts)

    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]
    completion = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        temperature=temperature,
    )
    return (completion.choices[0].message.content or "").strip()


def main() -> None:
    tests: List[TestCase] = [
        TestCase(
            name="Career pivot to data science",
            goal="Move into a data science role within a year with 5 years as a business analyst.",
            constraints="Can study 10 hours per week; prefer free or low-cost resources.",
            coach_style="Direct",
        ),
        TestCase(
            name="Overwhelmed by tasks",
            goal="Get more focused and finish tasks instead of starting many and finishing few.",
            constraints="",
            coach_style="Supportive",
        ),
        TestCase(
            name="Learn ML fundamentals",
            goal="Understand the fundamentals of machine learning.",
            constraints="3 months available; comfortable with Python.",
            coach_style="Analytical",
        ),
    ]

    print("Running Personal AI Coach prompt evaluation...\n")

    try:
        client = get_openai_client()
    except RuntimeError as err:
        print(f"Configuration error: {err}")
        return

    for idx, test in enumerate(tests, start=1):
        print(f"Test {idx}: {test.name}")
        print(f"  Coach style: {test.coach_style}")
        print(f"  Goal: {test.goal}")
        if test.constraints:
            print(f"  Constraints: {test.constraints}")
        print()

        try:
            response = run_test_case(client, test)
            status = "OK" if response else "EMPTY RESPONSE"
        except Exception as exc:
            response = f"[Error: {exc}]"
            status = "ERROR"

        print(f"  Status: {status}")
        print("  Response (first 500 chars):")
        print("   ", (response[:500] + ("..." if len(response) > 500 else "")))
        print("-" * 80)

    print("Evaluation complete.")


if __name__ == "__main__":
    main()
