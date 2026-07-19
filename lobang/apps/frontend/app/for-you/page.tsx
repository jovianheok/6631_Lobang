// For You page: personalized, preference-ranked deals for signed-in users.
// Redirects to /login if there is no active session, so it can't be reached
// (even by direct URL) while logged out.

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { supabase } from "@/lib/supabase";
import { getForYouDeals, type Deal } from "@/lib/api";
import DealCard from "@/components/deal-card";
import { useBookmarks } from "@/lib/use-bookmarks";

export default function ForYouPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isBookmarked, toggleBookmark } = useBookmarks();

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (!data.session) {
        router.replace("/login");
        return;
      }
      setReady(true);
      getForYouDeals()
        .then(setDeals)
        .catch(() => setError("Couldn't load your deals. Please try again."))
        .finally(() => setLoading(false));
    });
  }, [router]);

  if (!ready || loading) {
    return <main className="w-full max-w-2xl mx-auto p-6">Loading…</main>;
  }

  return (
    <main className="w-full max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold">For You</h1>
      <p className="text-gray-600">
        Deals ranked by how well they match your preferences.
      </p>

      {error ? (
        <p className="text-red-600">{error}</p>
      ) : deals.length === 0 ? (
        <p className="text-gray-600">
          No deals to show yet. Set your{" "}
          <Link href="/profile" className="text-blue-600 hover:underline">
            preferences
          </Link>{" "}
          to get personalized picks.
        </p>
      ) : (
        <div className="space-y-4">
          {deals.map((deal) => (
            <DealCard
              key={`${deal.id}-${deal.user_vote ?? "n"}-${deal.upvote_count}-${deal.downvote_count}`}
              {...deal}
              canVote
              bookmarked={isBookmarked(deal.id)}
              onToggleBookmark={() => toggleBookmark(deal.id)}
            />
          ))}
        </div>
      )}
    </main>
  );
}
