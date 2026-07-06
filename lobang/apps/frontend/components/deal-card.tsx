/*
  Props definition for the DealCard component.
  '?': optional
  '| null': value can explicitly be null
*/
type DealCardProps = {
  title: string;                                  // Main deal title
  merchant_name?: string | null;                  // Store name or merchant name
  description?: string | null;                    // Short description of the deal
  location_name?: string | null;                  // Location of the deal
  discount_value?: number | null;                 // Discount amount/value
  discount_unit?: string | null;                  // Discount unit (%, $, etc)
  source_url?: string | null;                     // External link to original sources
  distance_km?: number | null;                    // Distance from user in kilometres
  score?: number | null;                          // Ranking/relevance score
  cuisine?: string | null;                        // Cuisine label (Google Places)
  price_level?: number | null;                    // 0..4 price level
  display_location?: string | null;               // Frontend-friendly location label
  covered_regions?: string[];                     // SG regions the merchant covers
  bookmarked?: boolean;                           // Whether the user has saved this deal
  onToggleBookmark?: () => void;                  // Save/unsave handler (omit to hide button)
};


/*
  Functional React component that displays a single deal card.
*/
export default function DealCard({
  title,
  merchant_name,
  description,
  location_name,
  discount_value,
  discount_unit,
  source_url,
  distance_km,
  score,
  cuisine,
  price_level,
  display_location,
  covered_regions,
  bookmarked,
  onToggleBookmark,
}: DealCardProps) {
  // The scraper derives merchant_name from the title's leading prefix (e.g.
  // "KFC: 20% off" -> merchant "KFC"), so the raw title often repeats the
  // merchant. Strip a leading "<merchant><separator>" to avoid showing it twice.
  const displayTitle = (() => {
    if (!merchant_name) return title;
    const trimmed = title.trimStart();
    if (!trimmed.toLowerCase().startsWith(merchant_name.toLowerCase())) {
      return title;
    }
    const rest = trimmed.slice(merchant_name.length).replace(/^\s*[:\-–—|]\s*/, "");
    return rest.trim() || title;
  })();
  // Render price level as $ signs (1 -> $, 4 -> $$$$); null = unknown.
  const priceLabel =
    typeof price_level === "number" && price_level > 0
      ? "$".repeat(price_level)
      : null;
  // Color-grade the match score from green (strong) to yellow (weak). Score
  // ranges 0..5 (+2 cuisine, +2 region, +1 price).
  const scoreClass =
    typeof score === "number"
      ? score >= 4
        ? "bg-green-100 text-green-800"
        : score >= 2
        ? "bg-lime-100 text-lime-800"
        : "bg-yellow-100 text-yellow-800"
      : "";
  // Prefer an explicit display location, else fall back to covered regions.
  const locationLabel =
    display_location ??
    location_name ??
    (covered_regions && covered_regions.length > 0
      ? covered_regions.join(", ")
      : null);
  return (
    /*
      Outer card container
      - rounded corners
      - border
      - white background
      - padding
      - subtle shadow
    */
    <article className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm"> 

      {/* Top section: merchant info + optional score badge */}
      <div className="flex items-start justify-between gap-4">

        {/* Left side: merchant name and deal title */}
        <div>

          {/* Merchant name: primary heading, most prominent element */}
          <h2 className="text-xl font-bold tracking-tight text-gray-900">
            {merchant_name ?? "Unknown merchant"}
          </h2>

          {/* Deal title: supporting line under the merchant */}
          <p className="mt-1 text-base font-medium text-gray-700">
            {displayTitle}
          </p>
        </div>

        {/* Right side: optional score badge + save button */}
        <div className="flex shrink-0 items-center gap-2">
          {/* Match score, labeled and color-graded (green strong → yellow weak) */}
          {typeof score === "number" ? (
            <span
              className={`rounded-full px-3 py-1 text-sm font-medium ${scoreClass}`}
            >
              Score: {score}
            </span>
          ) : null}

          {/* Save/unsave button only renders when a handler is provided */}
          {onToggleBookmark ? (
            <button
              type="button"
              onClick={onToggleBookmark}
              aria-pressed={bookmarked}
              aria-label={bookmarked ? "Remove bookmark" : "Save deal"}
              className={`rounded-full border px-3 py-1 text-sm font-medium ${
                bookmarked
                  ? "border-black bg-black text-white"
                  : "border-gray-300 bg-white text-gray-700 hover:border-black"
              }`}
            >
              {bookmarked ? "♥ Saved" : "♡ Save"}
            </button>
          ) : null}
        </div>
      </div>

      {/* Optional deal description */}
      {description ? (
        <p className="mt-3 text-sm leading-6 text-gray-700 line-clamp-3">
          {description}
        </p>
      ) : null}

      {/* Metadata badges section */}
      <div className="mt-4 flex flex-wrap gap-2 text-sm text-gray-600">

        {/* Cuisine badge */}
        {cuisine ? (
          <span className="rounded-full bg-gray-100 px-3 py-1">{cuisine}</span>
        ) : null}

        {/* Price level badge */}
        {priceLabel ? (
          <span className="rounded-full bg-gray-100 px-3 py-1">{priceLabel}</span>
        ) : null}

        {/* Location badge */}
        {locationLabel ? (
          <span className="rounded-full bg-gray-100 px-3 py-1 capitalize">
            {locationLabel}
          </span>
        ) : null}

        {/* Discount badge */}
        {typeof discount_value === "number" ? (
          <span className="rounded-full bg-gray-100 px-3 py-1">
            {discount_value}
            {discount_unit ?? ""}
          </span>
        ) : null}

        {/* Distance badge */}
        {typeof distance_km === "number" ? (
          <span className="rounded-full bg-gray-100 px-3 py-1">
            {distance_km.toFixed(1)} km away
          </span>
        ) : null}
      </div>

      {/* External source link */}
      {source_url ? (               
        <div className="mt-4">
          <a
            href={source_url}
            target="_blank"
            rel="noreferrer"
            className="text-sm font-medium text-blue-600 hover:underline"
          >
            View source
          </a>
        </div>
      ) : null}
    </article>
  );
}
