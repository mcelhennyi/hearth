// @PROJ-U-* — @kindling/mantle main barrel (FR-0006 T-FR-0006-10 scaffold).
// Components and hooks land in T-FR-0006-11/12/13; overlay implementations in
// T-FR-0006-13; vanilla bridge in T-FR-0006-14. Type re-exports are kept here
// so consumers can import value-free types from the main entry today.
export type {
  ChromeButton,
  ChromeMenu,
  FrameState,
  ThemeTokens,
  InboundMessage,
  OutboundMessage,
} from "./types";

export {};
