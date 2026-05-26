import { useCallback } from "react";

import { useMantle } from "../MantleProvider";
import type { HapticStyle } from "../types";

export function useHaptics(): (style: HapticStyle) => void {
  const bridge = useMantle();
  return useCallback(
    (style: HapticStyle) => {
      bridge.post({ type: "hearth.haptic", style });
    },
    [bridge],
  );
}
