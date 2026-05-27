// Centralizes fetch logic here

const API_BASE_URL = "http://127.0.0.1:8000";


export async function getDeals() {
  const response = await fetch(                     // Sends HTTP request to backend and awaits backend response
    `${API_BASE_URL}/api/v1/deals`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch deals");
  }

  return response.json();                           // Converts JSON into JavaScript objects
}