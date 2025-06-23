// services/userService.ts

// 📦 Importation de la bibliothèque axios pour effectuer des requêtes HTTP
import axios from "axios";

// 🌍 URL de base de l'API backend (FastAPI ici). À adapter selon l'environnement (localhost ou serveur distant)
const API_URL = "http://localhost:8001"; // Par exemple : "https://api.monsite.com" en prod

// 🔐 Fonction utilitaire pour récupérer le token JWT du localStorage (stockage du navigateur)
// Le check `typeof window !== "undefined"` est nécessaire car dans certains contextes (ex: SSR avec Next.js),
// le code s'exécute côté serveur, et `window` n'existe pas
export const getToken = (): string | null => {
  if (typeof window !== "undefined") {
    return localStorage.getItem("token"); // Ou autre nom que tu utilises
  }
  return null;
};

// 🔄 Fonction pour récupérer tous les utilisateurs (admin uniquement)
export const getUsers = async () => {
  const token = getToken(); // 1️⃣ On récupère le token JWT stocké localement

  if (!token) {
    throw new Error("Utilisateur non authentifié : token manquant");
  }

  try {
    // 2️⃣ Appel HTTP vers l'API protégée avec le token dans le header
    const response = await axios.get(`${API_URL}/admin/users`, {
      headers: {
        Authorization: `Bearer ${token}`, // 🔐 Le backend va utiliser ce token pour vérifier l'identité
      },
    });

    // 3️⃣ Si tout est OK, on retourne les données (tableau d'utilisateurs)
    return response.data;
  } catch (error: any) {
    console.error("Erreur dans getUsers:", error?.response?.data || error.message);
    throw error; // On laisse le composant gérer l'affichage de l'erreur
  }
};


export const updateUserRole = async (userId: number, role: string) => {
  const token = getToken(); // 🔑 Récupère le token JWT de l'utilisateur connecté
  const response = await axios.put(
    `${API_URL}/admin/users/${userId}/role`, // 🛠️ URL de l'API pour modifier un rôle
    {
      role // 📤 Le nouveau rôle à envoyer au backend (envoyé dans le "body" en JSON)
    },
    {
      headers: {
        Authorization: `Bearer ${token}` // 🛡️ Authentification via token JWT
      }
    }
  );
  return response.data; // 📥 Retourne la réponse du backend (ex: message de confirmation)
}; 