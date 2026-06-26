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
}: DealCardProps) {
  // Render price level as $ signs (1 -> $, 4 -> $$$$); null = unknown.
  const priceLabel =
    typeof price_level === "number" && price_level > 0
      ? "$".repeat(price_level)
      : null;
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

          {/* Merchant name fallback if null/undefined */}
          <p className="text-sm font-medium text-gray-500">
            {merchant_name ?? "Unknown merchant"}
          </p>

          {/* Main deal title */}
          <h2 className="mt-1 text-xl font-semibold text-gray-900">
            {title}
          </h2>
        </div>

        {/* Show score only if score is a valid number */}
        {typeof score === "number" ? (
          <span className="rounded-full bg-gray-100 px-3 py-1 text-sm font-medium text-gray-700">
            {score}
          </span>
        ) : null}
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