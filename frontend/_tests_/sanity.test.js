// frontend/__tests__/sanity.test.js
import { render, screen } from "@testing-library/react";

test("affiche Hello World", () => {
  render(<div>Hello World</div>);
  expect(screen.getByText("Hello World")).toBeInTheDocument();
});
