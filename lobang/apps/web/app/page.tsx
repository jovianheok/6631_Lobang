import DealCard from "@/components/deal-card";
import { getDeals } from "@/lib/api";

export default async function HomePage() {
  const deals = await getDeals();                       // Calls backend API

  return (
    <main className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-3xl font-bold">
        Lobang
      </h1>

      {deals.map((deal: any) => (                       // Loops through deal array and renders one card for every deal
        <DealCard
          key={deal.id}
          title={deal.title}
          merchant_name={deal.merchant_name}
          distance_km={deal.distance_km}
          score={deal.score}
        />
      ))}
    </main>
  );
}