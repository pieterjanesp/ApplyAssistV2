import { useCallback, useEffect, useState } from 'react'
import { profileService } from '../../../services/profile.service'
import { useUserStore } from '../../../store/userStore'
import type { Profile } from '../../../types/profile'

export function useProfile() {
  const { profile, setProfile } = useUserStore()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchProfile = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await profileService.getProfile()
      setProfile(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load profile')
    } finally {
      setLoading(false)
    }
  }, [setProfile])

  useEffect(() => {
    if (!profile) {
      fetchProfile()
    }
  }, [profile, fetchProfile])

  const updateProfile = useCallback(
    async (data: Partial<Profile>) => {
      setLoading(true)
      try {
        const updated = await profileService.updateProfile(data)
        setProfile(updated)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to update profile')
      } finally {
        setLoading(false)
      }
    },
    [setProfile],
  )

  return { profile, loading, error, fetchProfile, updateProfile }
}
