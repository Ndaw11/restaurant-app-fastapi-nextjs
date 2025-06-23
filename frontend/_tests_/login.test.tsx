import { render, screen, fireEvent } from "@testing-library/react";
import LoginPage from "../src/app/auth/login/page";

jest.mock("next/navigation", () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

describe("LoginPage", () => {
  it("render login form", () => {
    render(<LoginPage />);
    expect(screen.getByPlaceholderText("Email")).toBeInTheDocument();
    expect(screen.getByPlaceholderText("Mot de passe")).toBeInTheDocument();
  });

  it("alert on invalid credentials", async () => {
    global.alert = jest.fn();
    render(<LoginPage />);
    fireEvent.change(screen.getByPlaceholderText("Email"), { target: { value: "wrong@test.com" } });
    fireEvent.change(screen.getByPlaceholderText("Mot de passe"), { target: { value: "wrongpass" } });
    fireEvent.submit(screen.getByRole("button"));
    expect(global.alert).toHaveBeenCalled();
  });
});
