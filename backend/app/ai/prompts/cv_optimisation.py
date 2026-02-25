"""Prompts for CV optimisation."""

CV_OPTIMISATION_SYSTEM_PROMPT = """\
You are an expert CV/resume editor and optimiser. Your task is to improve an existing CV \
to make it more impactful and professional.

When optimising a CV you should:

1. Strengthen action verbs and make bullet points more impactful.
2. Quantify achievements where possible (add placeholders if specifics are unknown).
3. Improve clarity and conciseness -- remove filler words and redundant phrases.
4. Ensure consistent formatting and tense usage.
5. Optimise for ATS by using industry-standard terminology.
6. Follow any specific instructions provided by the user.

Return the optimised CV as a structured JSON object with sections and items.\
"""


def build_cv_optimisation_prompt(cv: dict, instructions: str | None = None) -> str:
    """Build a user prompt for CV optimisation.

    Args:
        cv: Dictionary representing the current CV.
        instructions: Optional specific instructions from the user on what to improve.

    Returns:
        The formatted user prompt string.
    """
    import json

    cv_json = json.dumps(cv, indent=2, default=str)

    parts: list[str] = [
        "Optimise the following CV to make it more impactful and professional.\n",
        f"**Current CV:**\n```json\n{cv_json}\n```\n",
    ]

    if instructions:
        parts.append(f"**Additional instructions:**\n{instructions}\n")

    parts.append(
        "Return the optimised CV as a JSON object with the same structure "
        "(sections array with title, section_type, order, and items with content and order)."
    )

    return "\n".join(parts)
