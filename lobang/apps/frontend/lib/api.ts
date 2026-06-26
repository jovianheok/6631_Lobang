// Centralizes fetch logic here, contains all fetch calls to the FastAPI backend,
// base URL is read from environment variable

import { supabase } from "@/lib/supabase";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

// Build the Authorization header from the current Supabase session. Throws if the
// user isn't signed in, so callers can redirect to /login.
async function authHeaders(): Promise<Record<string, string>> {
  const { data } = await supabase.auth.getSession();
  const token = data.session?.access_token;
  if (!token) {
    throw new Error("Not authenticated");
  }
  return {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
  };
}

export async function getDeals() {
  const response = await fetch(                     // Sends HTTP request to backend and awaits backend response
    `${API_BASE_URL}/api/v1/deals`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch deals");
  }

  return response.json();                           // Converts JSON into JavaScript objects
}

// Shape of the preferences payload exchanged with the backend (mirrors
// PreferenceOut / PreferenceUpdate on the FastAPI side).
export type Preferences = {
  user_id: string;
  display_name: string | null;
  max_price_level: number | null;
  cuisine_preferences: string[];
  preferred_regions: string[];
  home_latitude: number | null;
  home_longitude: number | null;
  max_distance_km: number | null;
};

export async function getPreferences(): Promise<Preferences> {
  const response = await fetch(`${API_BASE_URL}/api/v1/preferences`, {
    headers: await authHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch preferences");
  }

  return response.json();
}

export async function updatePreferences(
  prefs: Omit<Preferences, "user_id">
): Promise<Preferences> {
  const response = await fetch(`${API_BASE_URL}/api/v1/preferences`, {
    method: "PUT",
    headers: await authHeaders(),
    body: JSON.stringify(prefs),
  });

  if (!response.ok) {
    throw new Error("Failed to update preferences");
  }

  return response.json();
}
