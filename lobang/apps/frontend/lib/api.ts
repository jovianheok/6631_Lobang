// Centralizes fetch logic here, contains all fetch calls to the FastAPI backend,
// base URL is read from environment variable

import { supabase } from "@/lib/supabase";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

function normalizeImageUrl(imageUrl: string | null): string | null {
  if (!imageUrl) return null;
  if (imageUrl.startsWith("http://") || imageUrl.startsWith("https://")) {
    return imageUrl;
  }
  return `${API_BASE_URL}${imageUrl}`;
}

function normalizeDeal(deal: Deal): Deal {
  return {
    ...deal,
    image_url: normalizeImageUrl(deal.image_url),
  };
}

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

async function optionalAuthHeaders(): Promise<Record<string, string> | undefined> {
  const { data } = await supabase.auth.getSession();
  const token = data.session?.access_token;
  if (!token) {
    return undefined;
  }
  return {
    Authorization: `Bearer ${token}`,
  };
}

// Shape of a deal returned by the backend (mirrors DealOut on the FastAPI side).
export type Deal = {
  id: number;
  title: string;
  merchant_name: string | null;
  source_url: string | null;
  more_info_url: string | null;
  image_url: string | null;
  time_text: string | null;
  start_date: string | null;
  end_date: string | null;
  upvote_count: number;
  downvote_count: number;
  community_score: number;
  user_vote: 1 | -1 | null;
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

export type DealVoteSummary = {
  deal_id: number;
  upvote_count: number;
  downvote_count: number;
  community_score: number;
  user_vote: 1 | -1 | null;
};

export async function getDeals(): Promise<Deal[]> {
  const response = await fetch(                     // Sends HTTP request to backend and awaits backend response
    `${API_BASE_URL}/api/v1/deals`,
    {
      headers: await optionalAuthHeaders(),
    }
  );

  if (!response.ok) {
    throw new Error("Failed to fetch deals");
  }

  return (await response.json()).map(normalizeDeal);                           // Converts JSON into JavaScript objects
}

// Personalized, preference-ranked deals for the signed-in user. Requires auth.
export async function getForYouDeals(): Promise<Deal[]> {
  const response = await fetch(`${API_BASE_URL}/api/v1/deals/for-you`, {
    headers: await authHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to fetch For You deals");
  }

  return (await response.json()).map(normalizeDeal);
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

  return (await response.json()).map(normalizeDeal);
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

export async function setDealVote(
  dealId: number,
  vote: 1 | -1
): Promise<DealVoteSummary> {
  const response = await fetch(`${API_BASE_URL}/api/v1/deals/${dealId}/vote`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify({ vote }),
  });

  if (!response.ok) {
    throw new Error("Failed to save vote");
  }

  return response.json();
}

export async function removeDealVote(dealId: number): Promise<DealVoteSummary> {
  const response = await fetch(`${API_BASE_URL}/api/v1/deals/${dealId}/vote`, {
    method: "DELETE",
    headers: await authHeaders(),
  });

  if (!response.ok) {
    throw new Error("Failed to remove vote");
  }

  return response.json();
}

// --- Submissions ---------------------------------------------------------------

// Submit a user deal. The backend runs it through the same parsing/enrichment
// pipeline as scraped Telegram posts and returns the published deal, or rejects
// with 422 (not recognised as a food deal) / 409 (duplicate) — those messages
// are surfaced to the caller.
export async function submitDeal(payload: {
  merchant_name: string;
  description: string;
  more_info_url?: string;
}): Promise<Deal> {
  const response = await fetch(`${API_BASE_URL}/api/v1/submissions`, {
    method: "POST",
    headers: await authHeaders(),
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    let message = "Failed to submit deal. Please try again.";
    try {
      const body = await response.json();
      if (typeof body.detail === "string") message = body.detail;
    } catch {
      // non-JSON error body; keep the generic message
    }
    throw new Error(message);
  }

  return response.json();
}
