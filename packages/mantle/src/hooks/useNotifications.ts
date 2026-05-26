import { useCallback } from "react";

import { useMantle } from "../MantleProvider";
import type { OutboundNotifyMessage } from "../types";

export function useNotifications(): (
  payload: OutboundNotifyMessage["payload"],
) => void {
  const bridge = useMantle();
  return useCallback(
    (payload: OutboundNotifyMessage["payload"]) => {
      bridge.post({ type: "hearth.notify", payload });
    },
    [bridge],
  );
}
