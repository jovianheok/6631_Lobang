// Maps browser geolocation coordinates to one of the five Singapore regions in
// lib/constants REGIONS, by nearest region centroid. Centroids are anchored on
// the same neighbourhoods the scraper's REGION_KEYWORDS uses, so "near me"
// matching agrees with how deals are enriched.

import { REGIONS } from "@/lib/constants";

export type Region = (typeof REGIONS)[number];

const REGION_CENTROIDS: Record<Region, { lat: number; lng: number }> = {
  north: { lat: 1.43, lng: 103.79 }, // Woodlands / Yishun
  south: { lat: 1.27, lng: 103.82 }, // HarbourFront / Bukit Merah
  east: { lat: 1.35, lng: 103.94 }, // Tampines / Bedok
  west: { lat: 1.34, lng: 103.71 }, // Jurong / Clementi
  central: { lat: 1.31, lng: 103.84 }, // Orchard / Novena
};

export function regionFromCoords(lat: number, lng: number): Region {
  let best: Region = "central";
  let bestDist = Infinity;
  for (const region of REGIONS) {
    const centroid = REGION_CENTROIDS[region];
    // Squared distance in degrees is a fine comparator at Singapore scale.
    const dist = (lat - centroid.lat) ** 2 + (lng - centroid.lng) ** 2;
    if (dist < bestDist) {
      bestDist = dist;
      best = region;
    }
  }
  return best;
}
