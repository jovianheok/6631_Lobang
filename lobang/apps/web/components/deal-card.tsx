// reusable React component that renders one UI card when a <DealCard.../> object is passed as input

type DealCardProps = {
  title: string;
  merchant_name: string;
  distance_km: number;
  score: number;
};

export default function DealCard({
  title,
  merchant_name,
  distance_km,
  score,
}: DealCardProps) {
  return (
    <div className="border rounded-lg p-4 space-y-2">
      <h2 className="text-xl font-semibold">
        {title}
      </h2>

      <p>{merchant_name}</p>

      <p>{distance_km} km away</p>

      <p>Score: {score}</p>
    </div>
  );
}