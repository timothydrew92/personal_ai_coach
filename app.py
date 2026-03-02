import os

import streamlit as st
from openai import OpenAI

from prompts import (
    COACH_STYLES,
    COACH_STYLE_DESCRIPTIONS,
    PLAN_SYSTEM_TEMPLATE,
)


def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Please export it in your shell environment."
        )
    return OpenAI()


def generate_plan(
    goal: str,
    constraints: str,
    coach_style: str,
    temperature: float,
) -> str:
    if not goal.strip():
        return ""

    system_content = PLAN_SYSTEM_TEMPLATE.format(
        coach_style=coach_style,
        style_guidance=COACH_STYLE_DESCRIPTIONS[coach_style],
    )

    user_parts = [f"**Goal:** {goal.strip()}"]
    if constraints.strip():
        user_parts.append(f"**Constraints:** {constraints.strip()}")
    user_content = "\n\n".join(user_parts)

    client = get_openai_client()
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content},
    ]

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=temperature,
        )
    except Exception as exc:
        return f"Error calling OpenAI API: {exc}"

    return (completion.choices[0].message.content or "").strip()


def main() -> None:
    st.set_page_config(
        page_title="Personal AI Coach",
        page_icon="🧠",
        layout="centered",
    )

    st.title("Personal AI Coach")
    st.markdown("Define your goal and constraints, then generate a structured plan.")

    goal = st.text_area(
        "Goal (required)",
        placeholder="e.g. Ship a side project in 3 months while working full-time",
        height=120,
        help="Describe what you want to achieve.",
    )

    constraints = st.text_area(
        "Constraints (optional)",
        placeholder="e.g. Only 5 hours per week; no budget for tools",
        height=80,
        help="Any limits on time, money, or other resources.",
    )

    col1, col2 = st.columns(2)

    with col1:
        coach_style = st.selectbox(
            "Coach style",
            options=COACH_STYLES,
            help="Supportive, Direct, or Analytical.",
        )
        st.caption(COACH_STYLE_DESCRIPTIONS[coach_style])
    with col2:
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.05,
            help="Lower = more focused and consistent; higher = more varied.",
        )

    if st.button("Generate Plan"):
        if not goal.strip():
            st.error("Please enter a goal.")
            return
        try:
            with st.spinner("Generating plan…"):
                response = generate_plan(
                    goal=goal,
                    constraints=constraints,
                    coach_style=coach_style,
                    temperature=temperature,
                )
        except RuntimeError as e:
            st.error(str(e))
            return

        if response.startswith("Error calling"):
            st.error(response)
            return

        st.divider()
        st.subheader("Your Plan")
        st.markdown(response)


if __name__ == "__main__":
    main()
