import type { TextareaHTMLAttributes } from "react";
import { cn } from "../lib/cn";

export type TextAreaProps = TextareaHTMLAttributes<HTMLTextAreaElement> & {
  label?: string;
  hint?: string;
  error?: string;
};

/** Multi-line text input with optional label and validation message. @HRT-U-11 */
export function TextArea({ label, hint, error, className, id, ...rest }: TextAreaProps) {
  const inputId =
    id ?? (label ? `mantle-textarea-${label.replace(/\s+/g, "-").toLowerCase()}` : undefined);
  const hintId = hint && inputId ? `${inputId}-hint` : undefined;
  const errorId = error && inputId ? `${inputId}-error` : undefined;
  const describedBy = [hintId, errorId].filter(Boolean).join(" ") || undefined;

  const control = (
    <textarea
      id={inputId}
      className={cn("mantle-textarea", className)}
      aria-invalid={error ? true : undefined}
      aria-describedby={describedBy}
      {...rest}
    />
  );

  if (!label && !hint && !error) {
    return control;
  }

  return (
    <div className="mantle-field">
      {label && inputId ? (
        <label className="mantle-field__label" htmlFor={inputId}>
          {label}
        </label>
      ) : null}
      {control}
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
