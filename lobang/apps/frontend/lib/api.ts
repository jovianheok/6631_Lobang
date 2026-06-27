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

// Shape of a deal returned by the backend (mirrors DealOut on the FastAPI side).
export type Deal = {
  id: number;
  title: string;
  merchant_name: string | null;
  source_url: string | null;
  cuisine: string | null;
  price_level: number | null;
  address: string | null;
  covered_regions: string[];
  display_location: string | null;
  // Legacy/optional fields, currently unpopulated
  description: string | null;
  location_name: string | null;
  discount_value: number | null;
  discount_unit: string | null;
  distance_km: number | null;
  score: number | null;
};

export async function getDeals(): Promise<Deal[]> {
  const response = await fetch(                     // Sends HTTP request to backend and awaits backend response
    `${API_BASE_URL}/api/v1/deals`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch deals");
  }

  return response.json();                           // Converts JSON into JavaScript objects
}

// Personalized, preference-ranked deals for the signed-in user. Requires auth.
export async function getForYouDeals(): Promise<Deal[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/deals/for-you`, {
    headers: await authHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch For You deals");
  }

  return response.json();
}

// --- Bookmarks ---------------------------------------------------------------

// The deals the signed-in user has saved (mirrors GET /bookmarks → list[DealOut]).
export async function getBookmarks(): Promise<Deal[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/bookmarks`, {
    headers: await authHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch bookmarks");
  }

  return response.json();
}

// Save a deal for the current user. Backend treats a repeat save as a no-op.
export async function addBookmark(dealId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/v1/bookmarks`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({ deal_id: dealId }),
  });

  if (!response.ok) {
    throw new Error("Failed to save bookmark");
  }
}

// Remove a saved deal. Deleting a missing bookmark is a no-op on the backend.
export async function removeBookmark(dealId: number): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/api/v1/bookmarks/${dealId}`, {
    method: "DELETE",
    headers: await authHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to remove bookmark");
  }
}

// Shape of the preferences payload exchanged with the backend (mirrors
// PreferenceOut / PreferenceUpdate on the FastAPI side).
export type Preferences = {
  user_id: string;
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
