import { useEffect, useState } from "react";

import { applyThemeTokens } from "../applyThemeTokens";
import { useMantle } from "../MantleProvider";
import type { ThemeTokens } from "../types";

export interface UseThemeResult {
  tokens: ThemeTokens | null;
  mode: ThemeTokens["mode"] | null;
}

export function useTheme(applyToDocument = true): UseThemeResult {
  const bridge = useMantle();
  const [tokens, setTokens] = useState<ThemeTokens | null>(null);

  useEffect(() => {
    return bridge.subscribe("hearth.theme", (msg) => {
      setTokens(msg.tokens);
      if (applyToDocument) applyThemeTokens(msg.tokens);
    });
  }, [bridge, applyToDocument]);

  return {
    tokens,
    mode: tokens?.mode ?? null,
  };
}
