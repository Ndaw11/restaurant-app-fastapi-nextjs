import { render, screen } from "@testing-library/react";
import AdminUsersPage from "../src/app/admin/users/page";

jest.mock("../../src/services/userService", () => ({
  getUsers: () => Promise.resolve([
    { id: 1, name: "Admin", email: "admin@test.com", role: "admin" }
  ]),
  updateUserRole: jest.fn()
}));

describe("AdminUsersPage", () => {
  it("affiche liste des utilisateurs", async () => {
    render(<AdminUsersPage />);
    const name = await screen.findByText("Admin");
    expect(name).toBeInTheDocument();
  });
});
