import { defineConfig } from "tsup";

// @PROJ-U-* — Mantle build config (FR-0006 T-FR-0006-10 scaffold, T-FR-0006-14 IIFE).
// ESM + CJS + .d.ts for library entries; IIFE global for <script>-tag plugins.
const shared = {
  dts: { compilerOptions: { ignoreDeprecations: "6.0" } },
  sourcemap: true,
  clean: true,
  splitting: false,
  treeshake: true,
  target: "es2022" as const,
  external: ["react", "react-dom"],
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
