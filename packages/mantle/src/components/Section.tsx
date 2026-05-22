import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type SectionProps = HTMLAttributes<HTMLElement> & {
  title?: string;
  children: ReactNode;
};

/** Grouped content with optional section label. @HRT-U-11 */
export function Section({ title, children, className, ...rest }: SectionProps) {
  return (
    <section className={cn("mantle-section", className)} {...rest}>
      {title ? <h2 className="mantle-section__title">{title}</h2> : null}
      {children}
    </section>
  );
}
