// Shared bookmark state for deal-listing views (Home, For You). Resolves the
// signed-in user's saved deal ids once, then exposes an optimistic toggle that
// reverts if the backend call fails. When signed out, the toggle is a no-op and
// nothing should render a save button.

"use client";

import { useCallback, useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";
import { getBookmarks, addBookmark, removeBookmark } from "@/lib/api";

export function useBookmarks() {
  const [signedIn, setSignedIn] = useState(false);
  const [bookmarkedIds, setBookmarkedIds] = useState<Set<number>>(new Set());

  useEffect(() => {
    let active = true;
    supabase.auth.getSession().then(({ data }) => {
      if (!active || !data.session) return;
      setSignedIn(true);
      getBookmarks()
        .then((deals) => {
          if (active) setBookmarkedIds(new Set(deals.map((d) => d.id)));
        })
        .catch(() => {
          /* leave the set empty; saving still works */
        });
    });
    return () => {
      active = false;
    };
  }, []);

  const isBookmarked = useCallback(
    (dealId: number) => bookmarkedIds.has(dealId),
    [bookmarkedIds]
  );

  const toggleBookmark = useCallback(
    async (dealId: number) => {
      const wasSaved = bookmarkedIds.has(dealId);

      // Optimistically update, then reconcile with the backend.
      setBookmarkedIds((prev) => {
        const next = new Set(prev);
        if (wasSaved) next.delete(dealId);
        else next.add(dealId);
        return next;
      });

      try {
        if (wasSaved) await removeBookmark(dealId);
        else await addBookmark(dealId);
      } catch {
        // Revert on failure.
        setBookmarkedIds((prev) => {
          const next = new Set(prev);
          if (wasSaved) next.add(dealId);
          else next.delete(dealId);
          return next;
        });
      }
    },
    [bookmarkedIds]
  );

  return { signedIn, isBookmarked, toggleBookmark };
}
