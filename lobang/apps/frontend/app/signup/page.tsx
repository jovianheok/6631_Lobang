// Signup form to take email and password and then create a supabase account.

 "use client";

  import { useState } from "react";
  import { useRouter } from "next/navigation";
  import { supabase } from "@/lib/supabase";
  import Link from "next/link";

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
        <main className="max-w-sm mx-auto p-6">
          <h1 className="text-2xl font-bold">Check your email</h1>
          <p className="mt-2 text-gray-600">
            We sent a confirmation link to <strong>{email}</strong>. Click it to activate your account.
          </p>
        </main>
      );
    }
    
    return (
      <main className="max-w-sm mx-auto p-6 space-y-4">
        <h1 className="text-2xl font-bold">Create an account</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input type="email" placeholder="Email" value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border p-2 rounded" />
          <input type="password" placeholder="Password" value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full border p-2 rounded" />
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button type="submit" className="w-full bg-black text-white p-2 rounded">
            Sign up
          </button>
        </form>
        <p className="text-sm text-center text-gray-500">
          Already have an account? <Link href="/login" className="underline">Log in</Link>
        </p>
      </main>
    );
  }
