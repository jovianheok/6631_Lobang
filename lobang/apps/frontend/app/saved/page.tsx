// Saved page: the deals the signed-in user has bookmarked. Redirects to /login
// if there is no active session. Unsaving removes the deal from the list.

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { supabase } from "@/lib/supabase";
import { getBookmarks, removeBookmark, type Deal } from "@/lib/api";
import DealCard from "@/components/deal-card";

export default function SavedPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);
  const [deals, setDeals] = useState<Deal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (!data.session) {
        router.replace("/login");
        return;
      }
      setReady(true);
      getBookmarks()
        .then(setDeals)
        .catch(() => setError("Couldn't load your saved deals. Please try again."))
        .finally(() => setLoading(false));
    });
  }, [router]);

  async function unsave(dealId: number) {
    const previous = deals;
    // Optimistically drop it from the list, restore if the request fails.
    setDeals((current) => current.filter((d) => d.id !== dealId));
    try {
      await removeBookmark(dealId);
    } catch {
      setDeals(previous);
    }
  }

  if (!ready || loading) {
    return <main className="w-full max-w-2xl mx-auto p-6">Loading…</main>;
  }

  return (
    <main className="w-full max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold">Saved</h1>
      <p className="text-gray-600">Deals you&apos;ve bookmarked.</p>

      {error ? (
        <p className="text-red-600">{error}</p>
      ) : deals.length === 0 ? (
        <p className="text-gray-600">
          You haven&apos;t saved any deals yet. Browse{" "}
          <Link href="/" className="text-blue-600 hover:underline">
            deals
          </Link>{" "}
          and tap Save.
        </p>
      ) : (
        <div className="space-y-4">
          {deals.map((deal) => (
            <DealCard
              key={`${deal.id}-${deal.user_vote ?? "n"}-${deal.upvote_count}-${deal.downvote_count}`}
              {...deal}
              canVote
              bookmarked
              onToggleBookmark={() => unsave(deal.id)}
            />
          ))}
        </div>
      )}
    </main>
  );
}
