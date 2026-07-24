import { describe, it, expect } from "vitest";
import { useState } from "react";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import CuisinePicker, {
  EMPTY_CUISINE_SELECTION,
  type CuisineSelection,
} from "@/components/cuisine-picker";

// CuisinePicker is controlled; this harness holds the selection state so clicks
// re-render it the way the real Home/Profile pages do.
function Harness() {
  const [selection, setSelection] =
    useState<CuisineSelection>(EMPTY_CUISINE_SELECTION);
  return <CuisinePicker selection={selection} onChange={setSelection} />;
}

describe("CuisinePicker", () => {
  it("shows the general group chips and hides specifics initially", () => {
    render(<Harness />);
    expect(screen.getByRole("button", { name: "Asian" })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Western" })).toBeInTheDocument();
    // A specific cuisine is not shown until its group is selected.
    expect(
      screen.queryByRole("button", { name: "Japanese" })
    ).not.toBeInTheDocument();
  });

  it("reveals a group's specific cuisines after selecting the group", async () => {
    const user = userEvent.setup();
    render(<Harness />);

    await user.click(screen.getByRole("button", { name: "Asian" }));

    expect(
      screen.getByRole("button", { name: "Japanese" })
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Chinese" })).toBeInTheDocument();
  });

  it("hides the specifics again when the group is deselected", async () => {
    const user = userEvent.setup();
    render(<Harness />);

    const asian = screen.getByRole("button", { name: "Asian" });
    await user.click(asian);
    expect(screen.getByRole("button", { name: "Japanese" })).toBeInTheDocument();

    await user.click(asian);
    expect(
      screen.queryByRole("button", { name: "Japanese" })
    ).not.toBeInTheDocument();
  });
});
