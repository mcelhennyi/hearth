// @PROJ-U-* — @kindling/mantle main barrel (FR-0006 components T-11, hooks T-12).
// Import `@kindling/mantle/styles.css` and `@kindling/mantle/components.css` in app entry.
// Protocol types: `import type { … } from "@kindling/mantle/types"`.

export type {
  ChromeButton,
  ChromeMenu,
  ChromePayload,
  ChromeRect,
  ChromeSlot,
  ChromeSurface,
  ChromeErrorReason,
  FrameState,
  ThemeTokens,
  UserInfo,
  InboundMessage,
  InboundType,
  InboundPayload,
  OutboundMessage,
  OutboundType,
  ToastLevel,
  HapticStyle,
  OverlayAction,
  PluginBridge,
} from "./types";
export { isInboundMessage } from "./types";
export { isAllowedMessageOrigin } from "./bridge";
export { createPluginBridge } from "./bridge";
export { applyThemeTokens } from "./applyThemeTokens";
export {
  MantleProvider,
  useMantle,
  useMantleOptional,
  useMantleBridge,
  useIsEmbedded,
} from "./MantleProvider";
export {
  useTheme,
  useUser,
  useChromeSlot,
  useHaptics,
  useNotifications,
  useSpark,
  type UseThemeResult,
  type UseChromeSlotOptions,
  type UseChromeSlotResult,
  type SparkHandle,
} from "./hooks";
export { Page, type PageProps } from "./components/Page";
export { PageHeader, type PageHeaderProps } from "./components/PageHeader";
export { Card, type CardProps } from "./components/Card";
export { Section, type SectionProps } from "./components/Section";
export { List, type ListProps } from "./components/List";
export { EmptyState, type EmptyStateProps } from "./components/EmptyState";
export { Button, type ButtonProps, type ButtonVariant } from "./components/Button";
export { IconButton, type IconButtonProps, type IconButtonVariant } from "./components/IconButton";
export { Input, type InputProps } from "./components/Input";
export { TextArea, type TextAreaProps } from "./components/TextArea";
export { Select, type SelectProps, type SelectOption } from "./components/Select";
export { Switch, type SwitchProps } from "./components/Switch";
export { Sheet, type SheetProps } from "./components/Sheet";
export { Dialog, type DialogProps } from "./components/Dialog";
export { Toast, type ToastProps } from "./components/Toast";
