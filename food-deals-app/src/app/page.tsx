import DealCard from "../components/DealCard";

export default function Home() {

  return (

    <main className="p-10">

      <h1 className="text-5xl font-bold">Food Deals</h1>

      <p className="mt-4 text-lg">

        Find the best food deals near you.

      </p>

      <div className="mt-10 grid gap-6">

        <DealCard

          title="2-for-1 Sushi"

          restaurant="Sakura Sushi"

          price="$15"

          cuisine="Japanese"

        />

        <DealCard

          title="$5 Burritos"

          restaurant="Taco Town"

          price="$5"

          cuisine="Mexican"

        />

        <DealCard

          title="Free Bubble Tea"

          restaurant="Tea Corner"

          price="Free"

          cuisine="Taiwanese"

        />

      </div>

    </main>

  );

}