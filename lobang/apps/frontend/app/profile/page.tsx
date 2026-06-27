// Profile page: lets a signed-in user edit their account credentials (email /
// password) and their deal preferences (price, cuisine, region). Redirects to
// /login if there is no active session.

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";
import {
  getPreferences,
  updatePreferences,
  type Preferences,
} from "@/lib/api";
import { CUISINES, REGIONS, PRICE_LEVELS } from "@/lib/constants";

export default function ProfilePage() {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [prefs, setPrefs] = useState<Preferences | null>(null);

  // Account fields
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [accountMsg, setAccountMsg] = useState("");

  // Preference save feedback
  const [savingPrefs, setSavingPrefs] = useState(false);
  const [prefsMsg, setPrefsMsg] = useState("");

  // Load session + preferences on mount.
  useEffect(() => {
    (async () => {
      const { data } = await supabase.auth.getSession();
      if (!data.session) {
        router.replace("/login");
        return;
      }
      setEmail(data.session.user.email ?? "");
      try {
        setPrefs(await getPreferences());
      } catch {
        setPrefsMsg("Could not load preferences.");
      } finally {
        setLoading(false);
      }
    })();
  }, [router]);

  function patch(update: Partial<Preferences>) {
    setPrefs((p) => (p ? { ...p, ...update } : p));
  }

  function toggleInList(key: "cuisine_preferences" | "preferred_regions", value: string) {
    if (!prefs) return;
    const current = prefs[key];
    patch({
      [key]: current.includes(value)
        ? current.filter((v) => v !== value)
        : [...current, value],
    } as Partial<Preferences>);
  }

  async function savePrefs(e: React.FormEvent) {
    e.preventDefault();
    if (!prefs) return;
    setSavingPrefs(true);
    setPrefsMsg("");
    try {
      const { user_id: _omit, ...payload } = prefs;
      const saved = await updatePreferences(payload);
      setPrefs(saved);
      setPrefsMsg("Preferences saved.");
    } catch {
      setPrefsMsg("Failed to save preferences.");
    } finally {
      setSavingPrefs(false);
    }
  }

  async function updateEmail() {
    setAccountMsg("");
    const { error } = await supabase.auth.updateUser({ email });
    setAccountMsg(error ? error.message : "Confirmation sent to the new email.");
  }

  async function updatePassword() {
    setAccountMsg("");
    if (newPassword.length < 6) {
      setAccountMsg("Password must be at least 6 characters.");
      return;
    }
    const { error } = await supabase.auth.updateUser({ password: newPassword });
    setAccountMsg(error ? error.message : "Password updated.");
    if (!error) setNewPassword("");
  }

  async function signOut() {
    await supabase.auth.signOut();
    router.replace("/login");
  }

  if (loading) {
    return <main className="max-w-2xl mx-auto p-6">Loading…</main>;
  }

  return (
    <main className="max-w-2xl mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Profile</h1>
        <button onClick={signOut} className="text-sm text-gray-500 underline">
          Sign out
        </button>
      </div>

      {/* ---- Account ---- */}
      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Account</h2>

        <label className="block text-sm font-medium">Email</label>
        <div className="flex gap-2">
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="flex-1 border p-2 rounded"
          />
          <button onClick={updateEmail} className="bg-black text-white px-4 rounded">
            Update
          </button>
        </div>

        <label className="block text-sm font-medium">New password</label>
        <div className="flex gap-2">
          <input
            type="password"
            value={newPassword}
            placeholder="••••••"
            onChange={(e) => setNewPassword(e.target.value)}
            className="flex-1 border p-2 rounded"
          />
          <button onClick={updatePassword} className="bg-black text-white px-4 rounded">
            Change
          </button>
        </div>

        {accountMsg && <p className="text-sm text-gray-600">{accountMsg}</p>}
      </section>

      {/* ---- Preferences ---- */}
      <form onSubmit={savePrefs} className="space-y-5">
        <h2 className="text-xl font-semibold">Preferences</h2>

        <div>
          <label className="block text-sm font-medium mb-1">Max price</label>
          <select
            value={prefs?.max_price_level ?? ""}
            onChange={(e) =>
              patch({ max_price_level: e.target.value === "" ? null : Number(e.target.value) })
            }
            className="w-full border p-2 rounded"
          >
            <option value="">Any</option>
            {PRICE_LEVELS.map((p) => (
              <option key={p.value} value={p.value}>
                {p.label}
              </option>
            ))}
          </select>
        </div>

        <fieldset>
          <legend className="text-sm font-medium mb-2">Cuisines</legend>
          <div className="flex flex-wrap gap-2">
            {CUISINES.map((c) => {
              const active = prefs?.cuisine_preferences.includes(c) ?? false;
              return (
                <button
                  type="button"
                  key={c}
                  onClick={() => toggleInList("cuisine_preferences", c)}
                  className={`px-3 py-1 rounded-full border text-sm ${
                    active ? "bg-black text-white" : "bg-white text-gray-700"
                  }`}
                >
                  {c}
                </button>
              );
            })}
          </div>
        </fieldset>

        <fieldset>
          <legend className="text-sm font-medium mb-2">Regions</legend>
          <div className="flex flex-wrap gap-2">
            {REGIONS.map((r) => {
              const active = prefs?.preferred_regions.includes(r) ?? false;
              return (
                <button
                  type="button"
                  key={r}
                  onClick={() => toggleInList("preferred_regions", r)}
                  className={`px-3 py-1 rounded-full border text-sm capitalize ${
                    active ? "bg-black text-white" : "bg-white text-gray-700"
                  }`}
                >
                  {r}
                </button>
              );
            })}
          </div>
        </fieldset>

        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={savingPrefs}
            className="bg-black text-white px-5 py-2 rounded disabled:opacity-50"
          >
            {savingPrefs ? "Saving…" : "Save preferences"}
          </button>
          {prefsMsg && <p className="text-sm text-gray-600">{prefsMsg}</p>}
        </div>
      </form>
    </main>
  );
}
