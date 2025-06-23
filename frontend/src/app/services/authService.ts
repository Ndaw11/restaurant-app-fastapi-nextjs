// services/authService.ts
import axios from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001"; // 🔁 Base de l’API

// 🔐 Connexion : envoie l'email et le mot de passe à FastAPI
export const loginUser = async (email: string, password: string) => {
  const params = new URLSearchParams();
  params.append("username", email);
  params.append("password", password);

  const response = await axios.post(`${API_URL}/token`, params, {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
  });

  const { access_token } = response.data;

  // Sauvegarde le token dans localStorage (ou cookie si tu veux plus tard)
  localStorage.setItem("token", access_token);
  return access_token;
};

// 📦 Récupère le token JWT stocké
export const getToken = () => {
  return localStorage.getItem("token");
};

// 🚪 Déconnexion : supprime le token
export const logoutUser = () => {
  localStorage.removeItem("token");
};
