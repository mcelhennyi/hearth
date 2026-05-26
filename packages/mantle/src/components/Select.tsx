import type { SelectHTMLAttributes } from "react";
import { cn } from "../lib/cn";

export type SelectOption = {
  value: string;
  label: string;
  disabled?: boolean;
};

export type SelectProps = SelectHTMLAttributes<HTMLSelectElement> & {
  label?: string;
  hint?: string;
  error?: string;
  options: SelectOption[];
};

/** Native select styled with hearth tokens. @HRT-U-11 */
export function Select({
  label,
  hint,
  error,
  options,
  className,
  id,
  ...rest
}: SelectProps) {
  const inputId = id ?? (label ? `mantle-select-${label.replace(/\s+/g, "-").toLowerCase()}` : undefined);
  const hintId = hint && inputId ? `${inputId}-hint` : undefined;
  const errorId = error && inputId ? `${inputId}-error` : undefined;
  const describedBy = [hintId, errorId].filter(Boolean).join(" ") || undefined;

  const control = (
    <select
      id={inputId}
      className={cn("mantle-select", className)}
      aria-invalid={error ? true : undefined}
      aria-describedby={describedBy}
      {...rest}
    >
      {options.map((opt) => (
        <option key={opt.value} value={opt.value} disabled={opt.disabled}>
          {opt.label}
        </option>
      ))}
    </select>
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
