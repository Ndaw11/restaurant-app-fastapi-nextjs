// pages/login.tsx
"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import { loginUser } from "../../services/authService";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await loginUser(email, password); // Appelle ton API pour obtenir le token
      router.push("/admin/users");      // Redirige après connexion réussie
    } catch {
      alert("Email ou mot de passe incorrect");
    }
  };

  return (
    <div className="max-w-md mx-auto p-6">
      <h1 className="text-2xl font-bold mb-4">Connexion</h1>
      <form onSubmit={handleLogin} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          className="border p-2 w-full"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Mot de passe"
          className="border p-2 w-full"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button className="bg-blue-600 text-white p-2 w-full" type="submit">
          Se connecter
        </button>
      </form>
    </div>
  );
}
