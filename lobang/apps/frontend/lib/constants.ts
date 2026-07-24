// Canonical option values mirrored from scraping/parsers/patterns.py so the UI's
// preference and filter options line up with how deals are enriched. Keep in sync
// with CUISINE_TYPE_MAP (values), REGION_ORDER, and PRICE_LEVEL_MAP there.

// Cuisine taxonomy: pickers show the general groups first and reveal a group's
// specific cuisines only while that group is selected. The specific values must
// match the scraper's CUISINE_TYPE_MAP outputs exactly (that's what deals store).
export const CUISINE_GROUPS: Record<string, readonly string[]> = {
  Asian: [
    "Chinese", "Japanese", "Korean", "Indian", "Thai", "Vietnamese",
    "Indonesian", "Malaysian", "Ramen", "Sushi",
  ],
  Western: [
    "Italian", "American", "French", "Mexican", "Mediterranean", "Pizza",
    "Burgers", "Sandwiches",
  ],
  Dietary: ["Vegetarian", "Vegan"],
  "Cafés & Desserts": ["Cafe", "Bakery", "Ice Cream", "Bubble Tea"],
  Miscellaneous: ["Seafood", "Bar", "Middle Eastern"],
};

// Flat list of every specific cuisine, derived so it can't drift from the groups.
export const CUISINES = Object.values(CUISINE_GROUPS).flat();

// Lowercase to match deals.covered_regions exactly; capitalize only for display.
export const REGIONS = ["north", "south", "east", "west", "central"] as const;

// max_price_level is "the most expensive I'm willing to see" (0..4).
export const PRICE_LEVELS = [
  { value: 1, label: "$" },
  { value: 2, label: "$$" },
  { value: 3, label: "$$$" },
  { value: 4, label: "$$$$" },
] as const;
