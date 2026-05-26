import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type EmptyStateProps = HTMLAttributes<HTMLDivElement> & {
  title: string;
  body?: string;
  icon?: ReactNode;
  action?: ReactNode;
};

/** Centered empty placeholder with optional CTA. @HRT-U-11 */
export function EmptyState({
  title,
  body,
  icon,
  action,
  className,
  ...rest
}: EmptyStateProps) {
  return (
    <div className={cn("mantle-empty-state", className)} role="status" {...rest}>
      {icon ? <div className="mantle-empty-state__icon" aria-hidden="true">{icon}</div> : null}
      <h2 className="mantle-empty-state__title">{title}</h2>
      {body ? <p className="mantle-empty-state__body">{body}</p> : null}
      {action ? <div className="mantle-empty-state__action">{action}</div> : null}
    </div>
  );
}
