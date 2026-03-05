import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import streamlit as st
from openai import OpenAI

from prompts import BASE_SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, PERSONA_OPTIONS

# Schema for structured coach response (JSON)
STRUCTURED_RESPONSE_INSTRUCTION = """
Respond with a single valid JSON object only, no other text or markdown. Use this exact structure (all string values in the chosen output language):
{"summary": "Brief user-friendly summary of the situation", "clarifying_questions": ["question 1", "question 2", ...], "next_steps": ["step 1", "step 2", ...], "motivational_message": "Optional short closing message or empty string"}
"""


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please set it before running the app."
        )
    return OpenAI(api_key=api_key)


def get_model_name() -> str:
    # Allow overriding the model via environment variable, but default to a sensible model.
    return os.getenv("OPENAI_MODEL", "gpt-4o")


def parse_structured_response(raw: str) -> Optional[Dict[str, Any]]:
    """Extract and parse JSON from model response; returns None if invalid."""
    text = raw.strip()
    # Remove optional markdown code fence
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        text = match.group(1).strip()
    try:
        data = json.loads(text)
        if isinstance(data, dict) and "summary" in data:
            return {
                "summary": data.get("summary", ""),
                "clarifying_questions": data.get("clarifying_questions") or [],
                "next_steps": data.get("next_steps") or [],
                "motivational_message": data.get("motivational_message") or "",
            }
    except (json.JSONDecodeError, TypeError):
        pass
    return None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def format_display_time(iso_str: str) -> str:
    """Format ISO timestamp for display (e.g. 'Mar 5, 2025 at 14:30')."""
    try:
        dt = datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
        return dt.strftime("%b %d, %Y at %H:%M")
    except (ValueError, AttributeError):
        return iso_str


# Output language options: highlighted (Hungarian, Spanish, Italian) first, then others
OUTPUT_LANGUAGES = [
    "English",
    "Hungarian",
    "Spanish",
    "Italian",
    "French",
    "German",
    "Portuguese",
    "Dutch",
    "Polish",
    "Japanese",
    "Chinese (Simplified)",
]


def build_messages(
    persona_id: str,
    goal: str,
    context: str,
    constraints: str,
    response_length: Optional[str] = None,
    tone: Optional[str] = None,
    challenge: Optional[str] = None,
    balance: Optional[str] = None,
    output_language: Optional[str] = None,
):
    persona = next(
        (p for p in PERSONA_OPTIONS if p["id"] == persona_id),
        PERSONA_OPTIONS[0],
    )
    example_phrases_str = "\n".join(f'- "{p}"' for p in persona.get("example_phrases", []))
    system_prompt = BASE_SYSTEM_PROMPT.format(
        persona_name=persona["persona_name"],
        style=persona.get("style", ""),
        focus=persona.get("focus", ""),
        emphasis=persona.get("emphasis", ""),
        avoid=persona.get("avoid", ""),
        example_phrases=example_phrases_str,
    )
    prefs = []
    if response_length:
        prefs.append(f"response length: {response_length}")
    if tone:
        prefs.append(f"tone: {tone}")
    if challenge:
        prefs.append(f"challenge level: {challenge}")
    if balance:
        prefs.append(f"balance: {balance}")
    if prefs:
        system_prompt += "\n\nUser preferences for this session: " + "; ".join(prefs) + "."
    if output_language and output_language != "English":
        system_prompt += f"\n\nRespond entirely in {output_language}. All of your output (summary, questions, next steps, and any motivational message) must be in {output_language}."
    system_prompt += "\n\n" + STRUCTURED_RESPONSE_INSTRUCTION
    user_prompt = USER_PROMPT_TEMPLATE.format(
        goal=goal.strip() or "No specific goal provided.",
        context=context.strip() or "No additional context provided.",
        constraints=constraints.strip() or "No explicit constraints provided.",
    )
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]


def _render_structured(data: Dict[str, Any]) -> None:
    """Render a structured coach response (summary, questions, steps, message)."""
    if data.get("summary"):
        st.markdown("**Summary**")
        st.write(data["summary"])
    if data.get("clarifying_questions"):
        st.markdown("**Clarifying questions**")
        for q in data["clarifying_questions"]:
            st.markdown(f"- {q}")
    if data.get("next_steps"):
        st.markdown("**Next steps**")
        for s in data["next_steps"]:
            st.markdown(f"- {s}")
    if data.get("motivational_message"):
        st.markdown("**Closing**")
        st.write(data["motivational_message"])


def init_session_state():
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "session_memory" not in st.session_state:
        st.session_state.session_memory = []


def main():
    st.set_page_config(page_title="Personal AI Coach", page_icon="💬")
    init_session_state()

    st.title("Personal AI Coach")
    st.write(
        "Use this minimal Streamlit app to experiment with a simple coaching persona "
        "powered by the OpenAI API. The coach remembers your conversation and key details as you build your plan."
    )

    with st.sidebar:
        st.header("Settings")
        persona_labels = [p["label"] for p in PERSONA_OPTIONS]
        selected_label = st.selectbox("Persona", persona_labels)
        selected_persona = next(
            p for p in PERSONA_OPTIONS if p["label"] == selected_label
        )
        if selected_persona.get("description"):
            st.caption(selected_persona["description"])

        st.subheader("Personality")
        response_length = st.radio(
            "Response length",
            options=["Short", "Medium", "Long"],
            index=1,
            help="Short = bullet points only; Long = more detail and examples.",
        )
        tone = st.selectbox(
            "Tone",
            options=["More casual", "Balanced", "More formal"],
            index=1,
            help="How formal or conversational the coach should sound.",
        )
        challenge = st.selectbox(
            "Challenge level",
            options=["Gentle", "Balanced", "Push harder"],
            index=1,
            help="How much to challenge assumptions and push for change.",
        )
        balance = st.selectbox(
            "Balance",
            options=["More questions", "Balanced", "More action steps"],
            index=1,
            help="Emphasize reflective questions vs concrete next steps.",
        )

        st.subheader("Output language")
        output_language = st.selectbox(
            "Language",
            options=OUTPUT_LANGUAGES,
            index=0,
            help="Coach responses will be generated in this language. Hungarian, Spanish, and Italian are highlighted as key options.",
        )
        if output_language in ("Hungarian", "Spanish", "Italian"):
            st.caption(f"✓ {output_language} selected")

        st.subheader("Model")
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative; lower = more focused.",
        )
        st.caption(f"Model: `{get_model_name()}` (set `OPENAI_MODEL` to override)")

        st.subheader("Memory")
        if st.button("Clear conversation & memory", type="secondary"):
            st.session_state.chat_history = []
            st.session_state.session_memory = []
            st.rerun()
        if st.session_state.session_memory:
            st.caption(f"{len(st.session_state.session_memory)} plan(s) with timestamps")
        if st.session_state.chat_history or st.session_state.session_memory:
            export = {
                "exported_at": now_iso(),
                "coaching_plans": st.session_state.chat_history,
                "session_memory": st.session_state.session_memory,
            }
            st.download_button(
                "Download session (JSON)",
                data=json.dumps(export, indent=2),
                file_name=f"coaching_session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
            )

    if st.session_state.chat_history:
        st.subheader("Coaching plans")
        i = 0
        while i < len(st.session_state.chat_history):
            msg = st.session_state.chat_history[i]
            role = msg.get("role", "user")
            content = msg.get("content", "")
            created_at = msg.get("created_at")
            time_label = format_display_time(created_at) if created_at else "Earlier"
            if role == "assistant":
                i += 1
                continue
            with st.expander(f"📋 Coaching plan — {time_label}", expanded=(i >= len(st.session_state.chat_history) - 2)):
                with st.chat_message("user"):
                    st.caption(time_label)
                    st.write(content)
                if i + 1 < len(st.session_state.chat_history) and st.session_state.chat_history[i + 1].get("role") == "assistant":
                    next_msg = st.session_state.chat_history[i + 1]
                    with st.chat_message("assistant"):
                        if next_msg.get("structured"):
                            _render_structured(next_msg["structured"])
                        else:
                            st.write(next_msg.get("content", ""))
                    i += 1
            i += 1

    goal = st.text_input(
        "What is your main goal?",
        placeholder="e.g. Get a promotion in 12 months, switch to a new career, run a marathon, learn a language, start a side business, improve work-life balance, get certified in a skill",
    )
    context = st.text_area(
        "What is your current situation?",
        placeholder="e.g. Current role, experience, company situation...",
    )
    constraints = st.text_area(
        "Any constraints or preferences?",
        placeholder="e.g. Limited time, remote only, preferred industries...",
    )

    if st.button("Get coaching advice"):
        if not goal.strip():
            st.warning("Please provide at least a brief goal so the coach can help.")
            return

        user_content = (
            f"**Goal:** {goal.strip()}\n\n"
            f"**Current situation:** {(context or 'Not provided.').strip()}\n\n"
            f"**Constraints or preferences:** {(constraints or 'None.').strip()}"
        )

        with st.spinner("Asking your personal AI coach..."):
            try:
                client = get_client()
                base_messages = build_messages(
                    persona_id=selected_persona["id"],
                    goal=goal,
                    context=context,
                    constraints=constraints,
                    response_length=response_length,
                    tone=tone,
                    challenge=challenge,
                    balance=balance,
                    output_language=output_language,
                )
                system_content = base_messages[0]["content"]
                if st.session_state.session_memory:
                    lines = []
                    for m in st.session_state.session_memory:
                        if isinstance(m, dict) and "created_at" in m:
                            lines.append(
                                f"- [{format_display_time(m['created_at'])}] Goal: {m.get('goal', '')}; Context: {m.get('context', '')}; Constraints: {m.get('constraints', '')}"
                            )
                        else:
                            lines.append(f"- {m}")
                    memory_block = "Session memory (key things we know about the user so far):\n" + "\n".join(lines)
                    system_content = system_content + "\n\n" + memory_block
                api_messages = [{"role": "system", "content": system_content}]
                for msg in st.session_state.chat_history:
                    api_messages.append({"role": msg["role"], "content": msg.get("content", "")})
                api_messages.append({"role": "user", "content": user_content})

                response = client.chat.completions.create(
                    model=get_model_name(),
                    messages=api_messages,
                    temperature=temperature,
                )
                content = response.choices[0].message.content or ""
                structured = parse_structured_response(content)
                created = now_iso()

                st.session_state.chat_history.append({
                    "created_at": created,
                    "role": "user",
                    "content": user_content,
                })
                st.session_state.chat_history.append({
                    "created_at": created,
                    "role": "assistant",
                    "content": content,
                    "structured": structured,
                })
                st.session_state.session_memory.append({
                    "created_at": created,
                    "goal": (goal or "").strip()[:200],
                    "context": (context or "").strip()[:200],
                    "constraints": (constraints or "").strip()[:200],
                })

                st.subheader("Coach response")
                if structured:
                    _render_structured(structured)
                else:
                    st.write(content)
                st.rerun()
            except Exception as exc:
                st.error(f"Error while contacting OpenAI API: {exc}")


if __name__ == "__main__":
    main()

