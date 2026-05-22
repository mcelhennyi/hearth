import type { InputHTMLAttributes } from "react";
import { cn } from "../lib/cn";

export type SwitchProps = Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  label: string;
};

/** Toggle switch using role=switch semantics. @HRT-U-11 */
export function Switch({ label, className, id, ...rest }: SwitchProps) {
  const switchId = id ?? `mantle-switch-${label.replace(/\s+/g, "-").toLowerCase()}`;

  return (
    <label className={cn("mantle-switch", className)} htmlFor={switchId}>
      <input
        type="checkbox"
        role="switch"
        id={switchId}
        className="mantle-switch__input"
        {...rest}
      />
      <span className="mantle-switch__track" aria-hidden="true">
        <span className="mantle-switch__thumb" />
      </span>
      <span className="mantle-switch__label">{label}</span>
    </label>
  );
}
