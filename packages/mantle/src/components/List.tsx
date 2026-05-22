import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type ListProps = HTMLAttributes<HTMLUListElement> & {
  children: ReactNode;
};

/** Styled list container for plugin rows. @HRT-U-11 */
export function List({ children, className, ...rest }: ListProps) {
  return (
    <ul className={cn("mantle-list", className)} {...rest}>
      {children}
    </ul>
  );
}
