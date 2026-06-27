// Public deal browser: fetches deals and filters them client-side by price,
// cuisine, and region. Filter options come from lib/constants so they match how
// deals are enriched. Fetching happens in the browser to avoid pulling the
// Supabase client into a server component.

"use client";

import { useEffect, useMemo, useState } from "react";
import DealCard from "@/components/deal-card";
import { getDeals, type Deal } from "@/lib/api";
import { CUISINES, REGIONS, PRICE_LEVELS } from "@/lib/constants";
import { useBookmarks } from "@/lib/use-bookmarks";

export default function DealsBrowser() {
  const [deals, setDeals] = useState<Deal[] | null>(null);
  const [maxPrice, setMaxPrice] = useState<number | null>(null);
  const [cuisines, setCuisines] = useState<string[]>([]);
  const [regions, setRegions] = useState<string[]>([]);
  const [filtersOpen, setFiltersOpen] = useState(false);
  const { signedIn, isBookmarked, toggleBookmark } = useBookmarks();

  useEffect(() => {
    getDeals()
      .then(setDeals)
      .catch(() => setDeals([]));
  }, []);

  function toggle(
    value: string,
    list: string[],
    setList: (next: string[]) => void
  ) {
    setList(list.includes(value) ? list.filter((v) => v !== value) : [...list, value]);
  }

  const filtered = useMemo(() => {
    if (!deals) return [];
    return deals.filter((d) => {
      // Price: keep deals at or below the chosen max (unknown price is excluded
      // when a max is set).
      if (maxPrice !== null && (d.price_level === null || d.price_level > maxPrice)) {
        return false;
      }
      // Cuisine: deal's single cuisine must be among the selected ones.
      if (cuisines.length > 0 && (d.cuisine === null || !cuisines.includes(d.cuisine))) {
        return false;
      }
      // Region: deal must cover at least one selected region.
      if (regions.length > 0 && !d.covered_regions.some((r) => regions.includes(r))) {
        return false;
      }
      return true;
    });
  }, [deals, maxPrice, cuisines, regions]);

  const activeCount =
    (maxPrice !== null ? 1 : 0) + cuisines.length + regions.length;
  const hasFilters = activeCount > 0;

  function clearAll() {
    setMaxPrice(null);
    setCuisines([]);
    setRegions([]);
  }

  return (
    <div className="space-y-6">
      {/* Filters (collapsible) */}
      <div className="rounded-2xl border border-gray-200">
        <div className="flex items-center justify-between p-4">
          <button
            type="button"
            onClick={() => setFiltersOpen((open) => !open)}
            aria-expanded={filtersOpen}
            className="flex items-center gap-2 text-sm font-semibold"
          >
            <span
              className={`inline-block transition-transform ${
                filtersOpen ? "rotate-90" : ""
              }`}
            >
              ▸
            </span>
            Filters
            {activeCount > 0 && (
              <span className="rounded-full bg-black px-2 py-0.5 text-xs font-medium text-white">
                {activeCount}
              </span>
            )}
          </button>
          {hasFilters && (
            <button onClick={clearAll} className="text-sm text-gray-500 underline">
              Clear
            </button>
          )}
        </div>

        {filtersOpen && (
        <div className="space-y-4 border-t border-gray-200 p-4">
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Max price</label>
          <select
            value={maxPrice ?? ""}
            onChange={(e) => setMaxPrice(e.target.value === "" ? null : Number(e.target.value))}
            className="border p-2 rounded text-sm"
          >
            <option value="">Any</option>
            {PRICE_LEVELS.map((p) => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>
        </div>

        <div>
          <p className="text-xs font-medium text-gray-500 mb-2">Cuisine</p>
          <div className="flex flex-wrap gap-2">
            {CUISINES.map((c) => (
              <button
                key={c}
                onClick={() => toggle(c, cuisines, setCuisines)}
                className={`px-3 py-1 rounded-full border text-sm ${
                  cuisines.includes(c) ? "bg-black text-white" : "bg-white text-gray-700"
                }`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>

        <div>
          <p className="text-xs font-medium text-gray-500 mb-2">Region</p>
          <div className="flex flex-wrap gap-2">
            {REGIONS.map((r) => (
              <button
                key={r}
                onClick={() => toggle(r, regions, setRegions)}
                className={`px-3 py-1 rounded-full border text-sm capitalize ${
                  regions.includes(r) ? "bg-black text-white" : "bg-white text-gray-700"
                }`}
              >
                {r}
              </button>
            ))}
          </div>
        </div>
        </div>
        )}
      </div>

      {/* Results */}
      {deals === null ? (
        <p className="text-gray-500">Loading deals…</p>
      ) : (
        <>
          <p className="text-sm text-gray-500">
            {filtered.length} deal{filtered.length === 1 ? "" : "s"}
            {hasFilters ? " match your filters" : ""}
          </p>
          {filtered.length === 0 ? (
            <p className="text-gray-500">No deals match your filters.</p>
          ) : (
            <div className="space-y-4">
              {filtered.map((deal) => (
                <DealCard
                  key={deal.id}
                  title={deal.title}
                  merchant_name={deal.merchant_name}
                  source_url={deal.source_url}
                  cuisine={deal.cuisine}
                  price_level={deal.price_level}
                  display_location={deal.display_location}
                  covered_regions={deal.covered_regions}
                  description={deal.description}
                  location_name={deal.location_name}
                  discount_value={deal.discount_value}
                  discount_unit={deal.discount_unit}
                  distance_km={deal.distance_km}
                  score={deal.score}
                  bookmarked={signedIn ? isBookmarked(deal.id) : undefined}
                  onToggleBookmark={
                    signedIn ? () => toggleBookmark(deal.id) : undefined
                  }
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
