"""Prompts for CV generation."""

CV_GENERATION_SYSTEM_PROMPT = """\
You are an expert CV/resume writer with deep knowledge of modern hiring practices, \
ATS (Applicant Tracking System) optimisation, and professional formatting standards.

Your task is to generate a well-structured, professional CV based on the user's profile \
information. The CV should:

1. Use clear, concise language with strong action verbs.
2. Quantify achievements wherever possible.
3. Be formatted with standard sections: Summary, Experience, Education, Skills, and optionally \
Projects and Certifications.
4. Be tailored to the target role or job description if provided.
5. Optimise for ATS compatibility by using standard section headers and relevant keywords.

Return the CV as a structured JSON object with sections and items.\
"""


def build_cv_generation_prompt(
    profile: dict,
    job_description: str | None = None,
) -> str:
    """Build a user prompt for CV generation.

    Args:
        profile: Dictionary containing user profile data (name, skills, experience, etc.).
        job_description: Optional job description to tailor the CV towards.

    Returns:
        The formatted user prompt string.
    """
    parts: list[str] = []

    parts.append("Generate a professional CV based on the following profile information:")
    parts.append(f"\n**Profile:**\n{_format_profile(profile)}")

    if job_description:
        parts.append(
            f"\n**Target Job Description:**\n{job_description}\n\n"
            "Please tailor the CV to highlight relevant experience and skills for this role."
        )

    parts.append(
        "\nReturn the result as a JSON object with a 'sections' array, where each section has "
        "'title', 'section_type', 'order', and an 'items' array with 'content' and 'order' fields."
    )

    return "\n".join(parts)


def _format_profile(profile: dict) -> str:
    """Format a profile dict into a readable string for the prompt."""
    lines: list[str] = []
    if name := profile.get("full_name"):
        lines.append(f"- Name: {name}")
    if email := profile.get("email"):
        lines.append(f"- Email: {email}")
    if phone := profile.get("phone"):
        lines.append(f"- Phone: {phone}")
    if location := profile.get("location"):
        lines.append(f"- Location: {location}")
    if summary := profile.get("summary"):
        lines.append(f"- Summary: {summary}")
    if skills := profile.get("skills"):
        lines.append(f"- Skills: {', '.join(skills)}")
    if years := profile.get("experience_years"):
        lines.append(f"- Years of experience: {years}")
    return "\n".join(lines) if lines else "(No profile data provided)"
