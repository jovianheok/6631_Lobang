// Creates and exports the Supabase client used i the browser, used by login and signup pages.
import { createBrowserClient } from "@supabase/ssr";

// Creates a single Supabase client instance using env vars from .env.local
// NEXT_PUBLIC_ prefix means that these are safe to expose to the browser.
  export const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  );
