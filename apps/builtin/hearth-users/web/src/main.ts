import "./styles.css";

const form = document.querySelector<HTMLFormElement>("#auth-form");
const message = document.querySelector<HTMLDivElement>("#message");
const username = document.querySelector<HTMLInputElement>("#username");
const displayName = document.querySelector<HTMLInputElement>("#display-name");
const password = document.querySelector<HTMLInputElement>("#password");
const button = form?.querySelector<HTMLButtonElement>("button");

function routeBase(): string {
  return window.location.pathname === "/hearth-users" ||
    window.location.pathname.startsWith("/hearth-users/")
    ? "/hearth-users"
    : "";
}

function endpoint(path: string): string {
  return `${routeBase()}${path}`;
}

function showMessage(kind: "ok" | "error", text: string): void {
  if (!message) return;
  message.dataset.kind = kind;
  message.dataset.visible = "true";
  message.textContent = text;
}

if (form && username && password && button) {
  form.dataset.setupEndpoint = endpoint("/api/setup");
  form.dataset.loginEndpoint = endpoint("/login");

  const params = new URLSearchParams(window.location.search);
  const next = params.get("next");
  form.dataset.next = next && next.startsWith("/") && !next.startsWith("//") ? next : "/";

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    button.disabled = true;
    showMessage("ok", form.dataset.mode === "setup" ? "Creating password..." : "Signing in...");

    try {
      const response = await fetch(
        form.dataset.mode === "setup"
          ? form.dataset.setupEndpoint ?? "/api/setup"
          : form.dataset.loginEndpoint ?? "/login",
        {
          method: "POST",
          credentials: "include",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            username: username.value,
            display_name:
              displayName && displayName.isConnected ? displayName.value : undefined,
            password: password.value,
          }),
        },
      );

      if (!response.ok) {
        let detail = "Sign in failed.";
        try {
          const payload = (await response.json()) as { detail?: unknown };
          if (typeof payload.detail === "string") detail = payload.detail;
        } catch (_error) {
          // Keep the generic message when the response is not JSON.
        }
        throw new Error(detail);
      }

      window.location.assign(form.dataset.next || "/");
    } catch (error) {
      showMessage("error", error instanceof Error ? error.message : "Sign in failed.");
      button.disabled = false;
      username.focus();
    }
  });
}
