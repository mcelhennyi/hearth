/**
 * LoginScreen — single-user login form for the Hearth hub.
 *
 * Authority: docs/design/mantle-ui.md (auth flow)
 *
 * Shows a password field and submits to POST /api/auth/login.
 * On success the parent (App.tsx) should re-check GET /api/auth/status
 * and render the authenticated shell.
 */

import { useState } from "react";

interface LoginScreenProps {
  onLogin: () => void;
}

export function LoginScreen({ onLogin }: LoginScreenProps) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const resp = await fetch("/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ password }),
      });
      if (resp.ok) {
        onLogin();
      } else if (resp.status === 429) {
        setError("Too many failed attempts. Please wait a minute and try again.");
      } else {
        setError("Invalid password.");
      }
    } catch {
      setError("Could not reach the hub. Check your network.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="hearth-login">
      <h1>Hearth</h1>
      <form onSubmit={handleSubmit}>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
          required
          disabled={loading}
        />
        {error && <p className="hearth-login__error">{error}</p>}
        <button type="submit" disabled={loading || !password}>
          {loading ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </div>
  );
}
