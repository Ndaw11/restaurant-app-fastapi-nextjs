"use client";

import { User } from "../interface/users";
import { updateUserRole } from "../services/userService";
import { useState } from "react";

interface Props {
  users: User[];
  setUsers: (users: User[]) => void;
}

export default function UserTable({ users, setUsers }: Props) {
  const handleRoleChange = async (userId: number, newRole: string) => {
    try {
      const updatedUser = await updateUserRole(userId, newRole);
      setUsers(users.map(u => (u.id === userId ? updatedUser : u)));
    } catch {
      alert("Erreur lors de la mise à jour");
    }
  };

  return (
    <table className="min-w-full border mt-6">
      <thead className="bg-gray-100">
        <tr>
          <th className="p-2 border">Nom</th>
          <th className="p-2 border">Email</th>
          <th className="p-2 border">Rôle</th>
          <th className="p-2 border">Modifier</th>
        </tr>
      </thead>
      <tbody>
        {users.map(user => (
          <tr key={user.id} className="border-t">
            <td className="p-2 border">{user.name}</td>
            <td className="p-2 border">{user.email}</td>
            <td className="p-2 border">{user.role}</td>
            <td className="p-2 border">
              <select
                value={user.role}
                onChange={e =>
                  handleRoleChange(user.id, e.target.value)
                }
                className="border p-1"
              >
                <option value="client">client</option>
                <option value="staff">staff</option>
                <option value="admin">admin</option>
              </select>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
