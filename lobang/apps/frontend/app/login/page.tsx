// Login and sign up page. Trackers whether the user is in "login" or "signup" mode. On Login,
// sign in via Supabase and redirects to homepage, else creates account and TODO: have 
// email verification

"use client"; // Uses interactivity (useState, form), so it runs in the browser

import { useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

type Mode = "login" | "signup";

export default function LoginPage() {
  const [mode, setMode] = useState<Mode>("login");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [signedUp, setSignedUp] = useState(false);
  const router = useRouter();


  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");

    if (mode === "login") {
      const { error } = await supabase.auth.signInWithPassword({ email, password });
      if (error) {
        setError(error.message);
      } else {
        router.refresh();
        router.push("/");
      }
    } else {
      const { data, error } = await supabase.auth.signUp({ email, password });
      if (error) {
        setError(error.message);
      } else if (data.session) {
        router.refresh();
        router.push("/");
      } else {
        setSignedUp(true);
      }
    }
  }

  if (signedUp) {
    return (
      <main className="max-w-sm mx-auto p-6 space-y-4 text-center">
        <h1 className="text-2xl font-bold">Check your email</h1>
        <p className="text-gray-600">
          We sent a confirmation link to <strong>{email}</strong>. Click it to activate your account.
        </p>
      </main>
    );
  }

  return (
    <main className="max-w-sm mx-auto p-6 space-y-4">
      <div className="flex border-b">
        <button
          className={`flex-1 pb-2 text-sm font-medium ${mode === "login" ? "border-b-2 border-black" : "text-gray-400"}`}
          onClick={() => { setMode("login"); setError(""); }}
        >
          Log in
        </button>
        <button
          className={`flex-1 pb-2 text-sm font-medium ${mode === "signup" ? "border-b-2 border-black" : "text-gray-400"}`}
          onClick={() => { setMode("signup"); setError(""); }}
        >
          Sign up
        </button>
      </div>

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
          {mode === "login" ? "Log in" : "Create account"}
        </button>
      </form>
    </main>
  );
}
