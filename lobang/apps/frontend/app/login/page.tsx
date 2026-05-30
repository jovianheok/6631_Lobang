"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const router = useRouter();

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const result = await supabase.auth.signInWithPassword({ email, password });
    if (result.error) {
      setError(result.error.message);
    } else {
      router.refresh();
      router.push("/");
    }
  }

  return (
    <main className="max-w-sm mx-auto p-6 space-y-4">
    <h1 className="text-2xl font-bold">Log in</h1>
    <form onSubmit={handleSubmit} className="space-y-4">
    <input
    type="email"
    placeholder="Email"
    value={email}
    onChange={(e) => setEmail(e.target.value)}
    className="w-full border p-2 rounded"
    />
    <input
    type="password"
    placeholder="Password"
    value={password}
    onChange={(e) => setPassword(e.target.value)}
    className="w-full border p-2 rounded"
    />
    {error && <p className="text-red-500 text-sm">{error}</p>}
    <button type="submit" className="w-full bg-black text-white p-2 rounded">
    Log in
    </button>
    </form>
    </main>
  );
}
