// Interface TypeScript qui définit la structure d'un utilisateur
// Le mot-clé 'export' permet d'exporter cette interface pour qu'elle puisse être importée dans d'autres fichiers
export interface User {
  // Identifiant unique de l'utilisateur (nombre entier)
  id: number;
  
  // Nom complet de l'utilisateur (chaîne de caractères)
  name: string;
  
  // Adresse email de l'utilisateur (chaîne de caractères)
  email: string;
  
  // Rôle de l'utilisateur dans l'application
  // Utilise un type union qui limite les valeurs possibles à seulement ces 3 options
  role: "client" | "staff" | "admin";
}