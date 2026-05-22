// @PROJ-U-* — @kindling/mantle main barrel (FR-0006 T-FR-0006-10 scaffold, hooks T-12).

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
