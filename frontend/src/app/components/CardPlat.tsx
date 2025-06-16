import React from 'react';

export default function CardPlat({ title, description, price }) {
  return (
    <div className="border rounded p-4 shadow-md max-w-xs">
      <h2 className="text-lg font-semibold mb-2">{title}</h2>
      <p className="mb-4">{description}</p>
      <p className="font-bold text-green-600">{price} FCFA</p>
    </div>
  );
}
