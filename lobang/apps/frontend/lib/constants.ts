// Canonical option values mirrored from scraping/parsers/patterns.py so the UI's
// preference and filter options line up with how deals are enriched. Keep in sync
// with CUISINE_TYPE_MAP (values), REGION_ORDER, and PRICE_LEVEL_MAP there.

export const CUISINES = [
  "Chinese", "Japanese", "Korean", "Indian", "Thai", "Italian", "American",
  "Mexican", "Seafood", "Vegetarian", "Vegan", "French", "Mediterranean",
  "Middle Eastern", "Vietnamese", "Indonesian", "Malaysian", "Ramen", "Sushi",
  "Pizza", "Burgers", "Sandwiches", "Bakery", "Cafe", "Bar", "Ice Cream",
  "Bubble Tea",
] as const;

// Lowercase to match deals.covered_regions exactly; capitalize only for display.
export const REGIONS = ["north", "south", "east", "west", "central"] as const;

// max_price_level is "the most expensive I'm willing to see" (0..4).
export const PRICE_LEVELS = [
  { value: 1, label: "$" },
  { value: 2, label: "$$" },
  { value: 3, label: "$$$" },
  { value: 4, label: "$$$$" },
] as const;
