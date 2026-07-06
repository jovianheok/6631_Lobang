// Two-tier cuisine picker: general groups (Asian, Western, …) show first, and a
// group's specific cuisines appear only while that group is selected.
//
// Selection semantics: a selected group with no chosen cuisines means
// "everything in the group"; choosing cuisines narrows it to just those.
// expandCuisineSelection turns a selection into the concrete cuisine list used
// for filtering (Home) and saving preferences (Profile), so the backend keeps
// exact-matching specific cuisine strings and needs no changes.

"use client";

import { CUISINE_GROUPS } from "@/lib/constants";

export type CuisineSelection = {
  groups: string[];   // selected general groups
  cuisines: string[]; // chosen specific cuisines within selected groups
};

export const EMPTY_CUISINE_SELECTION: CuisineSelection = { groups: [], cuisines: [] };

// Concrete cuisines a selection stands for: per group, its chosen cuisines, or
// all of the group's cuisines when none are chosen.
export function expandCuisineSelection({ groups, cuisines }: CuisineSelection): string[] {
  const expanded: string[] = [];
  for (const group of groups) {
    const children = CUISINE_GROUPS[group] ?? [];
    const chosen = children.filter((c) => cuisines.includes(c));
    expanded.push(...(chosen.length > 0 ? chosen : children));
  }
  return expanded;
}

// Rebuild picker state from a stored flat cuisine list (profile preferences):
// a group is selected if any of its cuisines are stored.
export function selectionFromCuisines(stored: string[]): CuisineSelection {
  const groups = Object.keys(CUISINE_GROUPS).filter((group) =>
    CUISINE_GROUPS[group].some((c) => stored.includes(c))
  );
  const cuisines = stored.filter((c) =>
    groups.some((group) => CUISINE_GROUPS[group].includes(c))
  );
  return { groups, cuisines };
}

type CuisinePickerProps = {
  selection: CuisineSelection;
  onChange: (next: CuisineSelection) => void;
};

export default function CuisinePicker({ selection, onChange }: CuisinePickerProps) {
  const { groups, cuisines } = selection;

  function toggleGroup(group: string) {
    if (groups.includes(group)) {
      // Deselecting a group also drops its chosen cuisines.
      onChange({
        groups: groups.filter((g) => g !== group),
        cuisines: cuisines.filter((c) => !CUISINE_GROUPS[group].includes(c)),
      });
    } else {
      onChange({ groups: [...groups, group], cuisines });
    }
  }

  function toggleCuisine(cuisine: string) {
    onChange({
      groups,
      cuisines: cuisines.includes(cuisine)
        ? cuisines.filter((c) => c !== cuisine)
        : [...cuisines, cuisine],
    });
  }

  return (
    <div className="space-y-3">
      {/* General groups */}
      <div className="flex flex-wrap gap-2">
        {Object.keys(CUISINE_GROUPS).map((group) => (
          <button
            type="button"
            key={group}
            onClick={() => toggleGroup(group)}
            className={`px-3 py-1 rounded-full border text-sm ${
              groups.includes(group) ? "bg-black text-white" : "bg-white text-gray-700"
            }`}
          >
            {group}
          </button>
        ))}
      </div>

      {/* Specific cuisines for each selected group */}
      {groups.map((group) => (
        <div key={group} className="border-l-2 border-gray-200 pl-3">
          <p className="mb-1 text-xs text-gray-500">{group}</p>
          <div className="flex flex-wrap gap-2">
            {(CUISINE_GROUPS[group] ?? []).map((c) => (
              <button
                type="button"
                key={c}
                onClick={() => toggleCuisine(c)}
                className={`px-3 py-1 rounded-full border text-sm ${
                  cuisines.includes(c) ? "bg-black text-white" : "bg-white text-gray-700"
                }`}
              >
                {c}
              </button>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
