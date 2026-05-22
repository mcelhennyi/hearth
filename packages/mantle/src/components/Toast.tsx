import { useEffect } from "react";

import { useMantleOptional } from "../MantleProvider";
import type { ToastLevel } from "../types";

export type ToastProps = {
  level?: ToastLevel;
  message: string;
};

/**
 * v0 toast stub (DG-U11): posts `hearth.toast` when embedded and console-logs.
 * Shell-side toast rendering is deferred.
 */
export function Toast({ level = "info", message }: ToastProps) {
  const bridge = useMantleOptional();

  useEffect(() => {
    // eslint-disable-next-line no-console -- DG-U11 v0 stub until shell renders toasts
    console.log("[mantle Toast]", { level, message });
    bridge?.post({ type: "hearth.toast", level, message });
  }, [bridge, level, message]);

  return null;
}
