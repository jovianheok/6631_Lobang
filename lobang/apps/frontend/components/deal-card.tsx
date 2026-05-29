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
}: DealCardProps) {
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

        {/* Location badge */}
        {location_name ? (
          <span className="rounded-full bg-gray-100 px-3 py-1">
            {location_name}
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