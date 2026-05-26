import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type PageProps = HTMLAttributes<HTMLElement> & {
  children: ReactNode;
};

/** Scrollable plugin frame root with safe-area insets. @HRT-U-11 */
export function Page({ children, className, ...rest }: PageProps) {
  return (
    <main className={cn("mantle-page", className)} {...rest}>
      <div className="mantle-page__inner">{children}</div>
    </main>
  );
}
