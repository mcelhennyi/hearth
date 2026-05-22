import { defineConfig } from "tsup";

// @PROJ-U-* — Mantle build config (FR-0006 T-FR-0006-10 scaffold).
// Produces ESM + CJS + .d.ts for three entry points: index, vanilla, types.
// CSS tokens (src/tokens.css) are consumed directly via the exports map
// (`./tokens`, `./styles.css`) and intentionally not bundled by tsup.
export default defineConfig({
  entry: {
    index: "src/index.ts",
    "vanilla/index": "src/vanilla/index.ts",
    types: "src/types.ts",
  },
  format: ["esm", "cjs"],
  dts: { compilerOptions: { ignoreDeprecations: "6.0" } },
  sourcemap: true,
  clean: true,
  splitting: false,
  treeshake: true,
  target: "es2022",
  external: ["react", "react-dom"],
});
