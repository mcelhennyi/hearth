import {
  createContext,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

import { createPluginBridge } from "./bridge";
import type { PluginBridge } from "./types";

const MantleContext = createContext<PluginBridge | null>(null);

export interface MantleProviderProps {
  children: ReactNode;
  /** Inject a bridge (tests). When omitted, one is created per provider mount. */
  bridge?: PluginBridge;
}

export function MantleProvider({ children, bridge: bridgeProp }: MantleProviderProps) {
  const [ownedBridge] = useState(() => bridgeProp ?? createPluginBridge());

  useEffect(() => {
    if (bridgeProp) return undefined;
    return () => ownedBridge.destroy();
  }, [bridgeProp, ownedBridge]);

  const value = bridgeProp ?? ownedBridge;
  return (
    <MantleContext.Provider value={value}>{children}</MantleContext.Provider>
  );
}

export function useMantle(): PluginBridge {
  const bridge = useContext(MantleContext);
  if (!bridge) {
    throw new Error("useMantle() requires a <MantleProvider> ancestor");
  }
  return bridge;
}

/** Optional access when a provider may be absent (e.g. Storybook). */
export function useMantleOptional(): PluginBridge | null {
  return useContext(MantleContext);
}

export function useMantleBridge(): PluginBridge {
  return useMantle();
}

export function useIsEmbedded(): boolean {
  const bridge = useMantle();
  return useMemo(() => bridge.embedded, [bridge.embedded]);
}
