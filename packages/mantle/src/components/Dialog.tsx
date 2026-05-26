import type { ReactNode } from "react";

import { OverlayFallback } from "./OverlayFallback";
import { useOverlayEscape } from "./useOverlayEscape";

export type DialogProps = {
  open: boolean;
  onOpenChange?: (open: boolean) => void;
  id?: string;
  title?: string;
  children: ReactNode;
};

/** Centered dialog that escapes the plugin iframe via postMessage when embedded. @HRT-U-13 */
export function Dialog({ open, onOpenChange, id, title, children }: DialogProps) {
  const escapeOpts = {
    ...(id !== undefined ? { id } : {}),
    ...(title !== undefined ? { title } : {}),
  };
  useOverlayEscape("dialog", open, escapeOpts);

  const close = () => onOpenChange?.(false);

  return (
    <OverlayFallback
      open={open}
      variant="dialog"
      {...(title !== undefined ? { title } : {})}
      onClose={close}
    >
      {children}
    </OverlayFallback>
  );
}
