import React from 'react';
import { render, screen } from '@testing-library/react';

test("affiche Hello World", () => {
  render(<div>Hello World</div>);
  expect(screen.getByText("Hello World")).toBeInTheDocument();
});
