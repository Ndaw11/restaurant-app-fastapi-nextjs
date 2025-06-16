"use client";
import React from "react";
import Navbar from "./components/Navbar";
import CardPlat from "./components/CardPlat";
import Button from "./components/Button";

export default function Accueil(){
  return(
    <>
    <Navbar></Navbar>
    <main className="p-4">
      <CardPlat  title="Poulet Yassa"
          description="Délicieux poulet mariné aux oignons et citron"
          price={3500}></CardPlat>
      <Button onClick={() => alert('Commande passée !')} className={''} children={'Acheter'}></Button>
    </main>
    </>
  );
}
