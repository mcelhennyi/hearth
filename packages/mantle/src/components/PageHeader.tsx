import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../lib/cn";

export type PageHeaderProps = HTMLAttributes<HTMLElement> & {
  title: string;
  subtitle?: string;
  /** Trailing actions (buttons, menus). */
  children?: ReactNode;
};

/** Page title block with optional subtitle and action slot. @HRT-U-11 */
export function PageHeader({
  title,
  subtitle,
  children,
  className,
  ...rest
}: PageHeaderProps) {
  return (
    <header className={cn("mantle-page-header", className)} {...rest}>
      <div className="mantle-page-header__row">
        <div>
          <h1 className="mantle-page-header__title">{title}</h1>
          {subtitle ? <p className="mantle-page-header__subtitle">{subtitle}</p> : null}
        </div>
        {children ? <div className="mantle-page-header__actions">{children}</div> : null}
      </div>
    </header>
  );
}
