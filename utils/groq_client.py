import streamlit as st
from groq import Groq

MODEL = "llama-3.3-70b-versatile"

SYSTEM_TEMPLATE = """You are TaxMind AI, a professional Indian tax advisor specialising in FY 2026 tax planning.
You have deep expertise in the Income Tax Act, GST, ITR filing, advance tax, and investment planning for Indian residents.

Current user context:
- Name: {name}
- Employment type: {employment_type}
- Income bracket: {income_bracket}
- Preferred tax regime: {preferred_regime}
- Total income recorded: Rs. {total_income:,.0f}
- Total expenses recorded: Rs. {total_expenses:,.0f}
- Estimated net tax payable: Rs. {net_tax:,.0f}

Instructions:
- Always give advice relevant to FY 2026 Indian tax rules.
- Be concise, accurate, and professional.
- Do not use emojis.
- Do not speculate. If you are unsure, say so and recommend consulting a CA.
- Cite relevant sections of the Income Tax Act where applicable.
- If the user asks about saving tax, focus on legal avenues valid under their chosen regime.
"""


def _build_system_prompt(context: dict) -> str:
    return SYSTEM_TEMPLATE.format(
        name=context.get("name", "User"),
        employment_type=context.get("employment_type", "Not specified"),
        income_bracket=context.get("income_bracket", "Not specified"),
        preferred_regime=context.get("preferred_regime", "new"),
        total_income=context.get("total_income", 0),
        total_expenses=context.get("total_expenses", 0),
        net_tax=context.get("net_tax", 0),
    )


def get_client() -> Groq:
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in .streamlit/secrets.toml")
    return Groq(api_key=api_key)


def chat(user_message: str, history: list[dict], context: dict) -> str:
    """
    Send a message to Groq and return the assistant reply as a string.

    Parameters
    ----------
    user_message : the latest user input
    history      : list of {role, content} dicts (prior turns)
    context      : dict with user financial context for system prompt

    Returns
    -------
    assistant reply string
    """
    client = get_client()

    system_prompt = _build_system_prompt(context)

    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=1000,
        temperature=0.4,
    )

    reply = response.choices[0].message.content
    return reply.strip()
