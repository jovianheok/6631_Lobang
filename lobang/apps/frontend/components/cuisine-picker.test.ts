import { describe, it, expect } from "vitest";
import {
  expandCuisineSelection,
  selectionFromCuisines,
  EMPTY_CUISINE_SELECTION,
} from "@/components/cuisine-picker";
import { CUISINE_GROUPS } from "@/lib/constants";

describe("expandCuisineSelection", () => {
  it("returns nothing for an empty selection", () => {
    expect(expandCuisineSelection(EMPTY_CUISINE_SELECTION)).toEqual([]);
  });

  it("expands a group with no specifics to all of its cuisines", () => {
    const expanded = expandCuisineSelection({ groups: ["Asian"], cuisines: [] });
    expect(expanded).toEqual([...CUISINE_GROUPS["Asian"]]);
  });

  it("narrows to only the chosen specifics within a selected group", () => {
    const expanded = expandCuisineSelection({
      groups: ["Asian"],
      cuisines: ["Japanese", "Korean"],
    });
    expect(expanded).toEqual(["Japanese", "Korean"]);
  });

  it("combines multiple groups, narrowing only where specifics are chosen", () => {
    const expanded = expandCuisineSelection({
      groups: ["Asian", "Dietary"],
      cuisines: ["Thai"],
    });
    // Asian narrowed to Thai; Dietary has no specifics so expands fully.
    expect(expanded).toEqual(["Thai", ...CUISINE_GROUPS["Dietary"]]);
  });
});

describe("selectionFromCuisines", () => {
  it("selects the groups whose cuisines appear in the stored list", () => {
    const selection = selectionFromCuisines(["Japanese", "Vegan"]);
    expect(selection.groups.sort()).toEqual(["Asian", "Dietary"]);
    expect(selection.cuisines.sort()).toEqual(["Japanese", "Vegan"]);
  });

  it("ignores unknown cuisines", () => {
    const selection = selectionFromCuisines(["Japanese", "NotACuisine"]);
    expect(selection.groups).toEqual(["Asian"]);
    expect(selection.cuisines).toEqual(["Japanese"]);
  });

  it("round-trips a narrowed selection through expand", () => {
    const stored = ["Japanese", "Korean"];
    const selection = selectionFromCuisines(stored);
    expect(expandCuisineSelection(selection).sort()).toEqual([...stored].sort());
  });
});
