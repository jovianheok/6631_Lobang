// Handle redirect back from Supabase after email confirmation, exchanges code in the URL for 
// a session, then sends the user to the homepage.

import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  // EXtract code query param from the URL
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");

  if (code) {
    // Access the cookie store so Supabase can save the sessio after exchanging the code
    const cookieStore = await cookies();
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll() {
            return cookieStore.getAll();
          },
          setAll(cookiesToSet) {
            // save the session cookies returned by Supabase
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            );
          },
        },
      }
    );
    // exchange the one-time code for a real session, logging in the user.
    await supabase.auth.exchangeCodeForSession(code);
  }

  // send the user to the homepage when they are logged in
  return NextResponse.redirect(new URL("/", request.url));
}
