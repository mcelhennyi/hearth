import { defineConfig } from "tsup";

// @PROJ-U-* — Mantle build config (FR-0006 T-10 scaffold, T-11 components, T-14 IIFE).
const shared = {
  dts: { compilerOptions: { ignoreDeprecations: "6.0" } },
  sourcemap: true,
  clean: true,
  splitting: false,
  treeshake: false,
  target: "es2022" as const,
  external: ["react", "react-dom"],
  esbuildOptions(options: { jsx?: string }) {
    options.jsx = "automatic";
  },
};

export default defineConfig([
  {
    ...shared,
    entry: {
      index: "src/index.ts",
      "vanilla/index": "src/vanilla/index.ts",
      types: "src/types.ts",
    },
    format: ["esm", "cjs"],
    platform: "browser",
  },
  {
    ...shared,
    entry: { "vanilla/mantle": "src/vanilla/global.ts" },
    format: ["iife"],
    globalName: "mantle",
    minify: false,
    dts: false,
    outExtension() {
      return { js: ".iife.js" };
    },
  },
]);
