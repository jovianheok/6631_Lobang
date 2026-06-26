// For You page: personalized deals for signed-in users. Redirects to /login if
// there is no active session, so it can't be reached (even by direct URL) while
// logged out. Curation is wired up once deal enrichment lands.

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

export default function ForYouPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (!data.session) {
        router.replace("/login");
      } else {
        setReady(true);
      }
    });
  }, [router]);

  if (!ready) {
    return <main className="max-w-2xl mx-auto p-6">Loading…</main>;
  }

  return (
    <main className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold">For You</h1>
      <p className="text-gray-600">
        Deals picked for you based on your preferences will appear here once deal
        enrichment is live.
      </p>
    </main>
  );
}
