"use client";
import React from "react";
import Navbar from "./components/Navbar";
import CardPlat from "./components/CardPlat";
import Button from "./components/Button";

export default function Accueil(){
  return(
    <>
      <Navbar/>
      <main className="p-4">
        <CardPlat/>
        <Button >
        </Button>
      </main>
    </>
  );
}
