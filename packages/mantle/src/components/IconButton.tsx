import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type IconButtonVariant = "default" | "accent" | "ghost";

export type IconButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  /** Required for icon-only controls (WCAG name). */
  "aria-label": string;
  variant?: IconButtonVariant;
  children: ReactNode;
};

const variantClass: Record<IconButtonVariant, string> = {
  default: "",
  accent: "mantle-icon-btn--accent",
  ghost: "mantle-icon-btn--ghost",
};

/** Icon-only control with 44×44px minimum hit target. @HRT-U-11 */
export function IconButton({
  variant = "default",
  className,
  type = "button",
  children,
  ...rest
}: IconButtonProps) {
  return (
    <button
      type={type}
      className={cn("mantle-icon-btn", variantClass[variant], className)}
      {...rest}
    >
      {children}
    </button>
  );
}
