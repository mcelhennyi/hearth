import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type CardProps = HTMLAttributes<HTMLDivElement> & {
  children: ReactNode;
};

/** Elevated surface card using `--hearth-surface`. @HRT-U-11 */
export function Card({ children, className, ...rest }: CardProps) {
  return (
    <div className={cn("mantle-card", className)} {...rest}>
      {children}
    </div>
  );
}
