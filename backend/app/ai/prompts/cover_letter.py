"""Prompts for cover letter generation."""

COVER_LETTER_SYSTEM_PROMPT = """\
You are an expert cover letter writer with deep understanding of professional communication \
and modern hiring practices.

When writing a cover letter you should:

1. Open with a compelling hook that shows genuine interest in the role.
2. Connect the candidate's experience and skills to the job requirements.
3. Demonstrate knowledge of the company where possible.
4. Use a tone that matches the requested style (professional, enthusiastic, conversational, etc.).
5. Keep the letter concise (3-4 paragraphs, ~300-400 words).
6. Close with a clear call to action.
7. Avoid generic phrases and cliches.

Return the cover letter as a plain text string.\
"""


def build_cover_letter_prompt(
    profile: dict,
    job_description: str,
    tone: str = "professional",
) -> str:
    """Build a user prompt for cover letter generation.

    Args:
        profile: Dictionary containing user profile data.
        job_description: The job description to write the cover letter for.
        tone: The desired tone of the cover letter.

    Returns:
        The formatted user prompt string.
    """
    profile_lines: list[str] = []
    if name := profile.get("full_name"):
        profile_lines.append(f"- Name: {name}")
    if summary := profile.get("summary"):
        profile_lines.append(f"- Summary: {summary}")
    if skills := profile.get("skills"):
        profile_lines.append(f"- Skills: {', '.join(skills)}")
    if years := profile.get("experience_years"):
        profile_lines.append(f"- Years of experience: {years}")

    profile_text = "\n".join(profile_lines) if profile_lines else "(No profile data)"

    return (
        f"Write a cover letter with a **{tone}** tone for the following job.\n\n"
        f"**Candidate Profile:**\n{profile_text}\n\n"
        f"**Job Description:**\n{job_description}\n\n"
        "Write the cover letter as plain text with proper paragraph breaks."
    )
