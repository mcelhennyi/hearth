/**
 * LoginScreen — handoff to the built-in hearth-users login route.
 *
 * Authority: tasks/feature-history/FR-0004-centralized-users-auth/10-design-01-gateway-and-trust.md
 *
 * Mantle consumers must not duplicate the password form. hearth-users owns
 * login, session cookies, and logout.
 */

interface LoginScreenProps {
  next?: string;
}

export function LoginScreen({ next = "/" }: LoginScreenProps) {
  const loginHref = `/hearth-users/login?next=${encodeURIComponent(next)}`;

  return (
    <div className="hearth-login">
      <h1>Hearth</h1>
      <a href={loginHref}>Sign in with Hearth Users</a>
    </div>
  );
}
