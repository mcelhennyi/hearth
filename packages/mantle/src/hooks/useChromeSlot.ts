import { useCallback, useEffect, useRef, useState } from "react";

import { useMantle } from "../MantleProvider";
import type {
  ChromeErrorReason,
  ChromePayload,
  ChromeRect,
  ChromeSlot,
  ChromeSurface,
} from "../types";

export interface UseChromeSlotOptions {
  onInvoke?: (detail: { id: string; itemId?: string }) => void;
  onResize?: (rect: ChromeRect) => void;
  onError?: (reason: ChromeErrorReason) => void;
}

export interface UseChromeSlotResult {
  mount: (payload: ChromePayload) => void;
  update: (payload: ChromePayload) => void;
  unmount: (id: string) => void;
  lastRect: ChromeRect | null;
  lastError: ChromeErrorReason | null;
}

export function useChromeSlot(
  slot: ChromeSlot,
  surface: ChromeSurface,
  options: UseChromeSlotOptions = {},
): UseChromeSlotResult {
  const bridge = useMantle();
  const optionsRef = useRef(options);
  optionsRef.current = options;
  const [lastRect, setLastRect] = useState<ChromeRect | null>(null);
  const [lastError, setLastError] = useState<ChromeErrorReason | null>(null);

  useEffect(() => {
    const unsubs = [
      bridge.subscribe("hearth.chrome.invoke", (msg) => {
        if (msg.slot !== slot || msg.surface !== surface) return;
        optionsRef.current.onInvoke?.({
          id: msg.id,
          ...(msg.itemId !== undefined ? { itemId: msg.itemId } : {}),
        });
      }),
      bridge.subscribe("hearth.chrome.resize", (msg) => {
        if (msg.slot !== slot) return;
        setLastRect(msg.rect);
        optionsRef.current.onResize?.(msg.rect);
      }),
      bridge.subscribe("hearth.chrome.error", (msg) => {
        if (msg.slot !== slot || msg.surface !== surface) return;
        setLastError(msg.reason);
        optionsRef.current.onError?.(msg.reason);
      }),
    ];
    return () => {
      for (const unsub of unsubs) unsub();
    };
  }, [bridge, slot, surface]);

  const mount = useCallback(
    (payload: ChromePayload) => {
      bridge.post({
        type: "hearth.chrome.mount",
        slot,
        surface,
        payload,
      });
    },
    [bridge, slot, surface],
  );

  const update = mount;

  const unmount = useCallback(
    (id: string) => {
      bridge.post({
        type: "hearth.chrome.unmount",
        slot,
        surface,
        id,
      });
    },
    [bridge, slot, surface],
  );

  return { mount, update, unmount, lastRect, lastError };
}
