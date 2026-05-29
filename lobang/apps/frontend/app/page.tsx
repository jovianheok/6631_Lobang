/*
  Import reusable DealCard component
  Used to display each individual deal
*/
import DealCard from "@/components/deal-card";

/*
  Import API helper function
  Fetches deals data from backend/database
*/
import { getDeals } from "@/lib/api";

/*
  Home page component
  'async' because data is fetched before rendering
*/
export default async function HomePage() {

  /* Fetch all available deals */
  const deals = await getDeals();

  return (
    /*
      Main page container
      - centered horizontally
      - maximum width
      - vertical spacing between elements
      - page padding
    */
    <main className="max-w-2xl mx-auto p-6 space-y-4">

      {/* Page title */}
      <h1 className="text-3xl font-bold">Lobang</h1>

      {/* Loop through all deals and render a DealCard for each one */}
      {deals.map((deal: any) => (
        <DealCard
          key={deal.id}                       // Unique React key for list rendering
          
          /* Deal information props */
          title={deal.title}
          merchant_name={deal.merchant_name}
          description={deal.description}
          location_name={deal.location_name}

          /* Discount information */
          discount_value={deal.discount_value}
          discount_unit={deal.discount_unit}

          /* External source link */
          source_url={deal.source_url}

          /* Distance from user */
          distance_km={deal.distance_km}

          /* Ranking/relevance score */
          score={deal.score}
        />
      ))}
    </main>
  );
}