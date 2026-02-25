"""Prompts for CV adaptation to specific job descriptions."""

CV_ADAPTATION_SYSTEM_PROMPT = """\
You are an expert CV/resume writer specialising in tailoring existing CVs to specific job \
descriptions. Your goal is to adapt the CV to maximise relevance without fabricating information.

When adapting a CV you should:

1. Reorder sections and items to prioritise the most relevant experience.
2. Adjust wording to incorporate keywords from the job description.
3. Emphasise transferable skills that match the job requirements.
4. Remove or de-emphasise less relevant content.
5. Ensure ATS compatibility with appropriate keywords.
6. Keep all information truthful -- do not invent experience or skills.

Return the adapted CV as a structured JSON object with sections and items.\
"""


def build_cv_adaptation_prompt(cv: dict, job_description: str) -> str:
    """Build a user prompt for CV adaptation.

    Args:
        cv: Dictionary representing the current CV (with sections and items).
        job_description: The target job description to adapt the CV for.

    Returns:
        The formatted user prompt string.
    """
    import json

    cv_json = json.dumps(cv, indent=2, default=str)

    return (
        "Adapt the following CV to better match the target job description.\n\n"
        f"**Current CV:**\n```json\n{cv_json}\n```\n\n"
        f"**Target Job Description:**\n{job_description}\n\n"
        "Return the adapted CV as a JSON object with the same structure "
        "(sections array with title, section_type, order, and items with content and order)."
    )
