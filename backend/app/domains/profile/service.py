"""Profile domain service layer."""

from app.core.supabase import get_supabase_client
from app.domains.profile.schemas import ProfileCreate, ProfileUpdate


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
        response = (
            self.client.table(self.TABLE)
            .insert(payload)
            .execute()
        )
        return response.data[0]

    def update_profile(self, user_id: str, data: ProfileUpdate) -> dict:
        """Update an existing profile and return the updated row."""
        payload = data.model_dump(exclude_unset=True)
        response = (
            self.client.table(self.TABLE)
            .update(payload)
            .eq("user_id", user_id)
            .execute()
        )
        return response.data[0]
