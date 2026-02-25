"""Pydantic AI agents for profile information extraction.

Each section has two agents:
  1. Interview agent (output_type=str) — conducts back-and-forth conversation
  2. Extraction agent (output_type=StructuredModel) — finalizes structured data

Model is deferred (not set at construction) so that:
  - No API key is needed at import time
  - The model can be configured via app settings at runtime
"""

from pydantic_ai import Agent

from app.domains.profile.extraction.deps import ExtractionContext
from app.domains.profile.schemas import (
    CareerGoalsCreate,
    EducationExtracted,
    SkillsExtracted,
    WorkExperienceExtracted,
)

DEFAULT_MODEL = "anthropic:claude-sonnet-4-20250514"

# ---------------------------------------------------------------------------
# Work Experience
# ---------------------------------------------------------------------------

work_experience_interview: Agent[ExtractionContext, str] = Agent(
    output_type=str,
    deps_type=ExtractionContext,
    system_prompt=(
        "You are a friendly career coach conducting a structured interview to learn about "
        "the user's work experience. Ask about their roles one at a time.\n\n"
        "For each role, gather:\n"
        "- Job title and company name\n"
        "- Start and end dates (or if it's their current role)\n"
        "- Key responsibilities and what the role involved\n"
        "- Notable achievements or accomplishments\n"
        "- Technologies or tools used\n\n"
        "Start by asking about their most recent or current role. After covering one role, "
        "ask if they have additional roles to discuss. Keep questions focused and one at a time. "
        "Be conversational but efficient."
    ),
)


@work_experience_interview.instructions
async def _work_exp_context(ctx: ExtractionContext) -> str:
    state = ctx.extracted_so_far
    parts = []
    if state.basic_info:
        parts.append(f"User: {state.basic_info.full_name}")
    if state.work_experiences:
        roles = ", ".join(f"{w.job_title} at {w.company}" for w in state.work_experiences)
        parts.append(f"Already captured work experiences: {roles}")
    return "\n".join(parts) if parts else ""


work_experience_extractor: Agent[ExtractionContext, WorkExperienceExtracted] = Agent(
    output_type=WorkExperienceExtracted,
    deps_type=ExtractionContext,
    system_prompt=(
        "Extract all work experience entries from the conversation below. "
        "Return structured data for each role discussed. "
        "If a field was not mentioned, leave it as null or empty. "
        "Dates should be formatted as 'YYYY-MM' or 'YYYY' if only the year was given."
    ),
)

# ---------------------------------------------------------------------------
# Education
# ---------------------------------------------------------------------------

education_interview: Agent[ExtractionContext, str] = Agent(
    output_type=str,
    deps_type=ExtractionContext,
    system_prompt=(
        "You are a friendly career coach conducting a structured interview to learn about "
        "the user's educational background. Ask about their qualifications one at a time.\n\n"
        "For each qualification, gather:\n"
        "- Institution name\n"
        "- Degree type (e.g., Bachelor's, Master's, PhD, Certificate)\n"
        "- Field of study / major\n"
        "- Start and end dates\n"
        "- Any notable details (honors, thesis topic, relevant coursework)\n\n"
        "Start with their highest or most recent qualification. After covering one, "
        "ask if they have more to discuss. Keep questions focused and one at a time."
    ),
)


@education_interview.instructions
async def _edu_context(ctx: ExtractionContext) -> str:
    state = ctx.extracted_so_far
    parts = []
    if state.basic_info:
        parts.append(f"User: {state.basic_info.full_name}")
    if state.work_experiences:
        roles = ", ".join(f"{w.job_title} at {w.company}" for w in state.work_experiences)
        parts.append(f"Work experience: {roles}")
    if state.education:
        edus = ", ".join(f"{e.degree} at {e.institution}" for e in state.education)
        parts.append(f"Already captured education: {edus}")
    return "\n".join(parts) if parts else ""


education_extractor: Agent[ExtractionContext, EducationExtracted] = Agent(
    output_type=EducationExtracted,
    deps_type=ExtractionContext,
    system_prompt=(
        "Extract all education entries from the conversation below. "
        "Return structured data for each qualification discussed. "
        "If a field was not mentioned, leave it as null or empty. "
        "Dates should be formatted as 'YYYY-MM' or 'YYYY' if only the year was given."
    ),
)

# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

skills_interview: Agent[ExtractionContext, str] = Agent(
    output_type=str,
    deps_type=ExtractionContext,
    system_prompt=(
        "You are a friendly career coach conducting a structured interview to learn about "
        "the user's skills and competencies.\n\n"
        "Cover these areas:\n"
        "- Technical skills (programming languages, frameworks, tools)\n"
        "- Soft skills (leadership, communication, problem-solving)\n"
        "- Domain expertise (industry-specific knowledge)\n"
        "- Certifications or notable qualifications\n\n"
        "Ask about one area at a time. Use their work experience and education "
        "(if available from context) to ask targeted follow-up questions. "
        "Be conversational but efficient."
    ),
)


@skills_interview.instructions
async def _skills_context(ctx: ExtractionContext) -> str:
    state = ctx.extracted_so_far
    parts = []
    if state.basic_info:
        parts.append(f"User: {state.basic_info.full_name}")
    if state.work_experiences:
        roles = ", ".join(f"{w.job_title} at {w.company}" for w in state.work_experiences)
        parts.append(f"Work experience: {roles}")
    if state.education:
        edus = ", ".join(f"{e.degree} at {e.institution}" for e in state.education)
        parts.append(f"Education: {edus}")
    if state.skills:
        parts.append(f"Already captured skills: {', '.join(state.skills)}")
    return "\n".join(parts) if parts else ""


skills_extractor: Agent[ExtractionContext, SkillsExtracted] = Agent(
    output_type=SkillsExtracted,
    deps_type=ExtractionContext,
    system_prompt=(
        "Extract all skills mentioned in the conversation below. "
        "Return a flat list of skill names. Include technical skills, soft skills, "
        "tools, frameworks, and domain expertise. Deduplicate and normalize names."
    ),
)

# ---------------------------------------------------------------------------
# Career Goals
# ---------------------------------------------------------------------------

career_goals_interview: Agent[ExtractionContext, str] = Agent(
    output_type=str,
    deps_type=ExtractionContext,
    system_prompt=(
        "You are a friendly career coach conducting a structured interview to learn about "
        "the user's career goals and aspirations.\n\n"
        "Cover these areas:\n"
        "- Target roles they're interested in\n"
        "- Industries or sectors they want to work in\n"
        "- Their career narrative — the story connecting their past to their future\n"
        "- Motivations — what drives them professionally\n"
        "- Preferred work style (remote, hybrid, on-site, startup vs corporate, etc.)\n\n"
        "Ask about one area at a time. Use their background (if available from context) "
        "to ask insightful follow-up questions. Be conversational but efficient."
    ),
)


@career_goals_interview.instructions
async def _goals_context(ctx: ExtractionContext) -> str:
    state = ctx.extracted_so_far
    parts = []
    if state.basic_info:
        parts.append(f"User: {state.basic_info.full_name}")
    if state.work_experiences:
        roles = ", ".join(f"{w.job_title} at {w.company}" for w in state.work_experiences)
        parts.append(f"Work experience: {roles}")
    if state.education:
        edus = ", ".join(f"{e.degree} at {e.institution}" for e in state.education)
        parts.append(f"Education: {edus}")
    if state.skills:
        parts.append(f"Skills: {', '.join(state.skills)}")
    return "\n".join(parts) if parts else ""


career_goals_extractor: Agent[ExtractionContext, CareerGoalsCreate] = Agent(
    output_type=CareerGoalsCreate,
    deps_type=ExtractionContext,
    system_prompt=(
        "Extract career goals from the conversation below. "
        "Return structured data covering target roles, target industries, "
        "career narrative, motivations, and preferred work style. "
        "If a field was not mentioned, leave it as null or empty."
    ),
)

# ---------------------------------------------------------------------------
# Registry for lookup by section name
# ---------------------------------------------------------------------------

INTERVIEW_AGENTS: dict[str, Agent] = {
    "work_experience": work_experience_interview,
    "education": education_interview,
    "skills": skills_interview,
    "career_goals": career_goals_interview,
}

EXTRACTION_AGENTS: dict[str, Agent] = {
    "work_experience": work_experience_extractor,
    "education": education_extractor,
    "skills": skills_extractor,
    "career_goals": career_goals_extractor,
}
