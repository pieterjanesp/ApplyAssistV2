"""Profile domain service layer."""

from app.core.supabase import get_supabase_client
from app.domains.profile.schemas import ExtractionState, ProfileCreate, ProfileUpdate


class ProfileService:
    """Service for managing user profiles via Supabase."""

    TABLE = "profiles"

    def __init__(self) -> None:
        self.client = get_supabase_client()

    def get_profile(self, user_id: str) -> dict | None:
        """Fetch a profile by user_id. Returns the row dict or None."""
        response = (
            self.client.table(self.TABLE)
            .select("*")
            .eq("user_id", user_id)
            .maybe_single()
            .execute()
        )
        return response.data

    def create_profile(self, user_id: str, data: ProfileCreate) -> dict:
        """Insert a new profile row and return it."""
        payload = data.model_dump()
        payload["user_id"] = user_id
        response = self.client.table(self.TABLE).insert(payload).execute()
        return response.data[0]

    def update_profile(self, user_id: str, data: ProfileUpdate) -> dict:
        """Update an existing profile and return the updated row."""
        payload = data.model_dump(exclude_unset=True)
        response = self.client.table(self.TABLE).update(payload).eq("user_id", user_id).execute()
        return response.data[0]

    def save_extraction(self, user_id: str, state: ExtractionState) -> dict:
        """Persist all extracted data to Supabase.

        Creates/updates the profile and inserts work experience, education,
        and career goals records.
        """
        # Upsert profile from basic_info + skills
        profile_data: dict = {}
        if state.basic_info:
            profile_data = state.basic_info.model_dump()
        if state.skills:
            profile_data["skills"] = state.skills

        existing = self.get_profile(user_id)
        if existing:
            if profile_data:
                profile = self.update_profile(user_id, ProfileUpdate(**profile_data))
            else:
                profile = existing
        else:
            if not profile_data.get("full_name"):
                profile_data["full_name"] = "Unknown"
            if not profile_data.get("email"):
                profile_data["email"] = "unknown@example.com"
            profile = self.create_profile(user_id, ProfileCreate(**profile_data))

        # Insert work experiences
        for we in state.work_experiences:
            payload = we.model_dump()
            payload["user_id"] = user_id
            self.client.table("work_experiences").insert(payload).execute()

        # Insert education records
        for edu in state.education:
            payload = edu.model_dump()
            payload["user_id"] = user_id
            self.client.table("education").insert(payload).execute()

        # Insert career goals
        if state.career_goals:
            payload = state.career_goals.model_dump()
            payload["user_id"] = user_id
            self.client.table("career_goals").insert(payload).execute()

        return profile
