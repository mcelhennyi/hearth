import { useEffect, useId } from "react";

import { useMantle } from "../MantleProvider";
import type { OverlayAction, OutboundDialogMessage, OutboundSheetMessage } from "../types";

export type OverlayKind = "sheet" | "dialog";

function overlayMessage(
  kind: OverlayKind,
  action: OverlayAction,
  id: string,
  title?: string,
): OutboundSheetMessage | OutboundDialogMessage {
  const base = { action, id, ...(title ? { title } : {}) };
  return kind === "sheet"
    ? { type: "hearth.sheet", ...base }
    : { type: "hearth.dialog", ...base };
}

/**
 * Posts open/close overlay messages to the parent shell when embedded.
 * Ticket T-FR-0006-13; spec: docs/design/mantle-ui.md §postMessage protocol.
 */
export function useOverlayEscape(
  kind: OverlayKind,
  open: boolean,
  options: { id?: string; title?: string },
): string {
  const bridge = useMantle();
  const autoId = useId();
  const overlayId = options.id ?? autoId;

  useEffect(() => {
    if (!bridge.embedded) return undefined;
    bridge.post(overlayMessage(kind, open ? "open" : "close", overlayId, options.title));
    return () => {
      if (open) {
        bridge.post(overlayMessage(kind, "close", overlayId, options.title));
      }
    };
  }, [bridge, kind, open, overlayId, options.title]);

  return overlayId;
}
