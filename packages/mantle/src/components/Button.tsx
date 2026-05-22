import type { ButtonHTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type ButtonVariant = "default" | "accent" | "ghost" | "danger";

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: ButtonVariant;
  block?: boolean;
  children: ReactNode;
};

const variantClass: Record<ButtonVariant, string> = {
  default: "",
  accent: "mantle-btn--accent",
  ghost: "mantle-btn--ghost",
  danger: "mantle-btn--danger",
};

/** Accessible button with 44px minimum touch target. @HRT-U-11 */
export function Button({
  variant = "default",
  block = false,
  className,
  type = "button",
  children,
  ...rest
}: ButtonProps) {
  return (
    <button
      type={type}
      className={cn(
        "mantle-btn",
        variantClass[variant],
        block && "mantle-btn--block",
        className,
      )}
      {...rest}
    >
      {children}
    </button>
  );
}
