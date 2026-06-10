// Centralizes fetch logic here, contains all fetch calls to the FastAPI backend,
// base URL is read from environment variable

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;


export async function getDeals() {
  const response = await fetch(                     // Sends HTTP request to backend and awaits backend response
    `${API_BASE_URL}/api/v1/deals`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch deals");
  }

  return response.json();                           // Converts JSON into JavaScript objects
}
