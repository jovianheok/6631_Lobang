import { describe, it, expect } from "vitest";
import { regionFromCoords } from "@/lib/geo";

describe("regionFromCoords", () => {
  // Coordinates sitting right on each region's anchor neighbourhood should map
  // back to that region.
  it.each([
    ["north", 1.43, 103.79], // Woodlands / Yishun
    ["south", 1.27, 103.82], // HarbourFront / Bukit Merah
    ["east", 1.35, 103.94], // Tampines / Bedok
    ["west", 1.34, 103.71], // Jurong / Clementi
    ["central", 1.31, 103.84], // Orchard / Novena
  ])("maps a point near %s to that region", (region, lat, lng) => {
    expect(regionFromCoords(lat, lng)).toBe(region);
  });

  it("resolves a real address to the nearest region", () => {
    // Tampines Mall (~1.3527, 103.9449) is clearly east.
    expect(regionFromCoords(1.3527, 103.9449)).toBe("east");
  });

  it("returns one of the five known regions for arbitrary coords", () => {
    const result = regionFromCoords(1.3, 103.85);
    expect(["north", "south", "east", "west", "central"]).toContain(result);
  });
});
