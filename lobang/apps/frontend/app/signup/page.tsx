// Signup form to take email and password and then create a supabase account.

"use client";

import Link from "next/link";
import { useState } from "react";

import { supabase } from "@/lib/supabase";

export default function SignupPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitted, setSubmitted] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const { error } = await supabase.auth.signUp({ email, password });
    if (error) {
      setError(error.message);
    } else {
      setSubmitted(true);
    }
  }

  if (submitted) {
    return (
      <main className="w-full max-w-sm mx-auto p-6">
        <h1 className="text-2xl font-bold">Check your email</h1>
        <p className="mt-2 text-gray-600">
          We sent a confirmation link to <strong>{email}</strong>. Click it to activate your account.
        </p>
      </main>
    );
  }

  return (
    <main className="w-full max-w-sm mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-bold">Create an account</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full rounded border p-2"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full rounded border p-2"
        />
        {error && <p className="text-sm text-red-500">{error}</p>}
        <button type="submit" className="w-full rounded bg-black p-2 text-white">
          Sign up
        </button>
      </form>
      <p className="text-center text-sm text-gray-500">
        Already have an account?{" "}
        <Link href="/login" className="underline">
          Log in
        </Link>
      </p>
    </main>
  );
}
