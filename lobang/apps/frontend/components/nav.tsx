// Top navigation. Home and For You show for everyone; Profile only appears when
// signed in. Subscribes to Supabase auth state so it updates on login/logout.

"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function Nav() {
  // null = still resolving session (avoids a flash of the wrong links)
  const [signedIn, setSignedIn] = useState<boolean | null>(null);

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSignedIn(!!data.session));
    const { data: sub } = supabase.auth.onAuthStateChange((_event, session) => {
      setSignedIn(!!session);
    });
    return () => sub.subscription.unsubscribe();
  }, []);

  return (
    <header className="border-b">
      <nav className="max-w-2xl mx-auto p-4 flex items-center gap-6 text-sm font-medium">
        <Link href="/" className="font-bold">Lobang</Link>
        <Link href="/for-you" className="text-gray-600 hover:text-black">For You</Link>
        {signedIn && (
          <Link href="/profile" className="text-gray-600 hover:text-black">Profile</Link>
        )}
        {signedIn === false && (
          <Link href="/login" className="ml-auto text-gray-600 hover:text-black">Log in</Link>
        )}
      </nav>
    </header>
  );
}
