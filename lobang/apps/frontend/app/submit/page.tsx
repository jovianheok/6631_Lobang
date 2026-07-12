// Submit page: signed-in users contribute deals. Submissions run through the
// same parsing/enrichment pipeline as scraped Telegram posts (classification,
// expiry/location extraction, Places enrichment), so a rejected submission
// surfaces the backend's reason and nothing is stored. Redirects to /login if
// there is no active session.

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import { submitDeal, type Deal } from "@/lib/api";
import DealCard from "@/components/deal-card";

export default function SubmitPage() {
  const router = useRouter();
  const [ready, setReady] = useState(false);

  const [merchant, setMerchant] = useState("");
  const [description, setDescription] = useState("");
  const [link, setLink] = useState("");

  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [created, setCreated] = useState<Deal | null>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => {
      if (!data.session) {
        router.replace("/login");
        return;
      }
      setReady(true);
    });
  }, [router]);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!merchant.trim() || !description.trim()) {
      setError("Merchant name and description are required.");
      return;
    }
    setSubmitting(true);
    setError(null);
    try {
      const deal = await submitDeal({
        merchant_name: merchant.trim(),
        description: description.trim(),
        more_info_url: link.trim() || undefined,
      });
      setCreated(deal);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit deal.");
    } finally {
      setSubmitting(false);
    }
  }

  function reset() {
    setMerchant("");
    setDescription("");
    setLink("");
    setCreated(null);
    setError(null);
  }

  if (!ready) {
    return <main className="w-full max-w-2xl mx-auto p-6">Loading…</main>;
  }

  // Success state: show the published deal exactly as it appears in the feed.
  if (created) {
    return (
      <main className="w-full max-w-2xl mx-auto p-6 space-y-4">
        <h1 className="text-3xl font-bold">Deal submitted</h1>
        <p className="text-gray-600">
          Thanks! Your deal is live — here&apos;s how it looks:
        </p>
        <DealCard {...created} />
        <button
          onClick={reset}
          className="bg-black text-white px-5 py-2 rounded"
        >
          Submit another
        </button>
      </main>
    );
  }

  return (
    <main className="w-full max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold">Submit a deal</h1>

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium mb-1">Merchant</label>
          <input
            type="text"
            value={merchant}
            onChange={(e) => setMerchant(e.target.value)}
            placeholder="e.g. KFC"
            className="w-full border p-2 rounded"
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Deal description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            rows={4}
            placeholder="e.g. 1-for-1 Zinger burger till 31 July, all outlets"
            className="w-full border p-2 rounded"
          />
          <p className="mt-1 text-xs text-gray-500">
            Include the offer, and the expiry date or outlet if you know them —
            they&apos;re picked up automatically.
          </p>
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Link <span className="text-gray-400">(optional)</span>
          </label>
          <input
            type="url"
            value={link}
            onChange={(e) => setLink(e.target.value)}
            placeholder="https://…"
            className="w-full border p-2 rounded"
          />
        </div>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={submitting}
          className="bg-black text-white px-5 py-2 rounded disabled:opacity-50"
        >
          {submitting ? "Checking & publishing…" : "Submit deal"}
        </button>
        {submitting && (
          <p className="text-sm text-gray-500">
            Verifying and enriching your deal — this can take a few seconds.
          </p>
        )}
      </form>
    </main>
  );
}
