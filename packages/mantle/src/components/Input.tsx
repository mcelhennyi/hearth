import type { InputHTMLAttributes } from "react";
import { cn } from "../lib/cn";

export type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  hint?: string;
  error?: string;
};

/** Text input with optional label, hint, and error. @HRT-U-11 */
export function Input({ label, hint, error, className, id, ...rest }: InputProps) {
  const inputId = id ?? (label ? `mantle-input-${label.replace(/\s+/g, "-").toLowerCase()}` : undefined);
  const hintId = hint && inputId ? `${inputId}-hint` : undefined;
  const errorId = error && inputId ? `${inputId}-error` : undefined;
  const describedBy = [hintId, errorId].filter(Boolean).join(" ") || undefined;

  if (!label && !hint && !error) {
    return (
      <input
        id={inputId}
        className={cn("mantle-input", className)}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        {...rest}
      />
    );
  }

  return (
    <div className="mantle-field">
      {label && inputId ? (
        <label className="mantle-field__label" htmlFor={inputId}>
          {label}
        </label>
      ) : null}
      <input
        id={inputId}
        className={cn("mantle-input", className)}
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        {...rest}
      />
      {hint ? (
        <span id={hintId} className="mantle-field__hint">
          {hint}
        </span>
      ) : null}
      {error ? (
        <span id={errorId} className="mantle-field__error" role="alert">
          {error}
        </span>
      ) : null}
    </div>
  );
}
