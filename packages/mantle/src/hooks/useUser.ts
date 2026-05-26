import { useEffect, useState } from "react";

import { useMantle } from "../MantleProvider";
import type { UserInfo } from "../types";

export function useUser(): UserInfo | null {
  const bridge = useMantle();
  const [user, setUser] = useState<UserInfo | null>(null);

  useEffect(() => {
    return bridge.subscribe("hearth.user", (msg) => {
      setUser(msg.user);
    });
  }, [bridge]);

  return user;
}
