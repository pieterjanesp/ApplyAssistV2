"""Prompts for extracting structured profile information from raw text."""

INFO_EXTRACTION_SYSTEM_PROMPT = """\
You are an expert at extracting structured information from unstructured text such as \
resumes, CVs, LinkedIn profiles, and personal bios.

Your task is to parse the provided text and extract the following fields:

- full_name: The person's full name.
- email: Email address, if present.
- phone: Phone number, if present.
- location: City/region/country, if present.
- summary: A brief professional summary (1-3 sentences).
- skills: A list of technical and professional skills mentioned.
- experience_years: Estimated total years of professional experience (integer).

Return the result as a JSON object with the above fields. Use null for any field that \
cannot be determined from the text.\
"""


def build_info_extraction_prompt(raw_text: str) -> str:
    """Build a user prompt for extracting profile info from raw text.

    Args:
        raw_text: The unstructured text to extract information from (e.g., pasted resume).

    Returns:
        The formatted user prompt string.
    """
    return (
        "Extract structured profile information from the following text.\n\n"
        f"**Text:**\n{raw_text}\n\n"
        "Return the result as a JSON object with the fields: "
        "full_name, email, phone, location, summary, skills (array), experience_years (integer). "
        "Use null for any fields that cannot be determined."
    )
