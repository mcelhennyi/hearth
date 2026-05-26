import { useEffect, type ReactNode } from "react";
import { createPortal } from "react-dom";

import type { OverlayKind } from "./useOverlayEscape";

export interface OverlayFallbackProps {
  open: boolean;
  variant: OverlayKind;
  title?: string;
  onClose: () => void;
  children: ReactNode;
}

/** In-iframe overlay when the shell does not host the surface (v0 default). */
export function OverlayFallback({
  open,
  variant,
  title,
  onClose,
  children,
}: OverlayFallbackProps) {
  useEffect(() => {
    if (!open) return undefined;
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open, onClose]);

  if (!open) return null;

  return createPortal(
    <div
      className={`mantle-overlay mantle-overlay--${variant}`}
      role={variant === "dialog" ? "dialog" : "presentation"}
      aria-modal="true"
      aria-labelledby={title ? "mantle-overlay-title" : undefined}
    >
      <button
        type="button"
        className="mantle-overlay__backdrop"
        aria-label="Close"
        onClick={onClose}
      />
      <div className={`mantle-overlay__panel mantle-overlay__panel--${variant}`}>
        {title ? (
          <header id="mantle-overlay-title" className="mantle-overlay__title">
            {title}
          </header>
        ) : null}
        <div className="mantle-overlay__body">{children}</div>
      </div>
    </div>,
    document.body,
  );
}
