import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import App from "./App";

describe("App Component", () => {
  it("renders Signova AI header", () => {
    render(<App />);
    expect(
      screen.getByText("Signova AI - Indian Sign Language Recognition")
    ).toBeDefined();
  });
});
