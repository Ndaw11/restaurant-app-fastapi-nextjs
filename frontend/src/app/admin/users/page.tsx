"use client";

import { useEffect, useState } from "react";
import { getUsers, updateUserRole } from "../../services/userService";
import { User } from "../../interface/users";
import { useRouter } from "next/navigation"; 


export default function AdminUsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
const router = useRouter();
useEffect(() => {
  
  getUsers()
    .then((data)=>{
      setUsers(data);
      setLoading(false)
    })
    .catch((error) => {
      console.error("Erreur lors du chargement des utilisateurs :", error);
      alert("Veuillez vous connecter pour voir les utilisateurs.");
      setLoading(false);
      router.push("/auth/login"); // redirection vers login si erreur auth
    });
}, []);


  const handleRoleChange = async (userId: number, newRole: string) => {
    try {
      const updatedUser = await updateUserRole(userId, newRole);
      setUsers(users.map(u => u.id === userId ? updatedUser : u));
    } catch {
      alert("Erreur lors du changement de rôle");
    }
  };

  if (loading) return <p className="p-4">Chargement...</p>;

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">👑 Dashboard Admin – Utilisateurs</h1>
      <table className="min-w-full border">
        <thead className="bg-gray-100">
          <tr>
            <th className="p-2 border">Nom</th>
            <th className="p-2 border">Email</th>
            <th className="p-2 border">Rôle</th>
            <th className="p-2 border">Modifier le rôle</th>
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
                  onChange={(e) => handleRoleChange(user.id, e.target.value)}
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
    </div>
  );
}
