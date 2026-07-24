/*
  Home page: public deal listing with price / cuisine / region filters.
  Deal fetching + filtering live in the client DealsBrowser component.
*/
import DealsBrowser from "@/components/deals-browser";

export default function HomePage() {
  return (
    <main className="w-full max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-3xl font-bold">Home</h1>
      <DealsBrowser />
    </main>
  );
}
