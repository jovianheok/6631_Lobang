//  Runs on every request before the page loads. Checks for a Supabase session and redirects
//  unauthenticated users to /login.
import { createServerClient } from "@supabase/ssr";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export async function proxy(req: NextRequest) {
  //start with a default "Pass through" reponse
  let res = NextResponse.next({ request: { headers: req.headers } });

  //create Supbase server client that can read and write cookies
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return req.cookies.getAll(); // read cookies from the incoming request
        },
        setAll(cookiesToSet) {
          // write updated cookies back to both the request and response
          cookiesToSet.forEach(({ name, value }) => req.cookies.set(name, value));
          res = NextResponse.next({ request: { headers: req.headers } });
          cookiesToSet.forEach(({ name, value, options }) =>
            res.cookies.set(name, value, options)
          );
        },
      },
    }
  );

  // check is the user has an active session
  const { data: { session } } = await supabase.auth.getSession();

  // pages that don't require login
  const isPublic =
    req.nextUrl.pathname.startsWith("/login") ||
    req.nextUrl.pathname.startsWith("/auth/callback");

  // if no session and page is not public, redirect to login
  if (!session && !isPublic) {
    return NextResponse.redirect(new URL("/login", req.url));
  }

  return res;
}
// apply this middlewre to all routes except Next internals, the favicon, and
// static asset files in public/ (e.g. the logo) — otherwise image requests get
// redirected to /login and fail to load.
export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp|ico)$).*)",
  ],
};
