import DealCard from "../components/DealCard";
import deals from "../data/collins-deals.json";

export default function Home() {
  return (
    <main className="p-10">
      <h1 className="text-5xl font-bold">Food Deals</h1>

      <p className="mt-4 text-lg">
        Find the best food deals near you.
      </p>

      <div className="mt-10 grid gap-6">
        {deals.map((deal, index) => (
          <DealCard
            key={`${deal.imageUrl}-${index}`}
            title={deal.title || "Untitled Deal"}
            restaurant={deal.source}
            price={deal.priceText || "Unknown"}
            cuisine={deal.cuisine || "Unknown"}
            imageUrl={deal.imageUrl}
          />
        ))}
      </div>
    </main>
  );
}