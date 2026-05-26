import type { ReactNode } from "react";

import { OverlayFallback } from "./OverlayFallback";
import { useOverlayEscape } from "./useOverlayEscape";

export type SheetProps = {
  open: boolean;
  onOpenChange?: (open: boolean) => void;
  /** Stable overlay id for shell deduplication; auto-generated when omitted. */
  id?: string;
  title?: string;
  children: ReactNode;
};

/** Bottom sheet that escapes the plugin iframe via postMessage when embedded. @HRT-U-13 */
export function Sheet({ open, onOpenChange, id, title, children }: SheetProps) {
  const escapeOpts = {
    ...(id !== undefined ? { id } : {}),
    ...(title !== undefined ? { title } : {}),
  };
  useOverlayEscape("sheet", open, escapeOpts);

  const close = () => onOpenChange?.(false);

  return (
    <OverlayFallback
      open={open}
      variant="sheet"
      {...(title !== undefined ? { title } : {})}
      onClose={close}
    >
      {children}
    </OverlayFallback>
  );
}
