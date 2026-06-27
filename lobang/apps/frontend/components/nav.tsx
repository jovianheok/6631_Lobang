// Top navigation. The Lobang wordmark sits at the top-left; Home and For You
// show for everyone; Saved and Profile only appear when signed in. The link for
// the page you're currently on is bolded. Subscribes to Supabase auth state so
// it updates on login/logout.

"use client";

import Link from "next/link";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function Nav() {
  // null = still resolving session (avoids a flash of the wrong links)
  const [signedIn, setSignedIn] = useState<boolean | null>(null);
  const pathname = usePathname();

  useEffect(() => {
    supabase.auth.getSession().then(({ data }) => setSignedIn(!!data.session));
    const { data: sub } = supabase.auth.onAuthStateChange((_event, session) => {
      setSignedIn(!!session);
    });
    return () => sub.subscription.unsubscribe();
  }, []);

  // Bold + dark for the active page, muted otherwise.
  const linkClass = (href: string) =>
    pathname === href
      ? "font-bold text-black"
      : "font-medium text-gray-600 hover:text-black";

  return (
    <header className="border-b">
      <div className="flex items-center gap-6 px-6 py-4 text-sm">
        <Link href="/" className="shrink-0">
          <Image src="/logo.jpeg" alt="Lobang" width={80} height={40} priority />
        </Link>

        <nav className="flex items-center gap-6">
          <Link href="/" className={linkClass("/")}>Home</Link>
          <Link href="/for-you" className={linkClass("/for-you")}>For You</Link>
          {signedIn && (
            <Link href="/saved" className={linkClass("/saved")}>Saved</Link>
          )}
          {signedIn && (
            <Link href="/profile" className={linkClass("/profile")}>Profile</Link>
          )}
        </nav>

        {signedIn === false && (
          <Link href="/login" className={`ml-auto ${linkClass("/login")}`}>
            Log in
          </Link>
        )}
      </div>
    </header>
  );
}
