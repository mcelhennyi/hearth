import { existsSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { describe, expect, it } from "vitest";
import pkg from "../package.json";

const pkgRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

function resolveExportTarget(subpath: string): string {
  const spec = pkg.exports as Record<
    string,
    string | { import?: string; require?: string; types?: string }
  >;
  const entry = spec[subpath];
  if (!entry) {
    throw new Error(`missing export: ${subpath}`);
  }
  if (typeof entry === "string") {
    return join(pkgRoot, entry.replace(/^\.\//, ""));
  }
  const rel = entry.import ?? entry.require ?? entry.types;
  if (!rel) {
    throw new Error(`export ${subpath} has no resolvable path`);
  }
  return join(pkgRoot, rel.replace(/^\.\//, ""));
}

describe("@kindling/mantle package scaffold", () => {
  it("exports map resolves to built artifacts and tokens CSS", () => {
    const main = resolveExportTarget(".");
    const vanilla = resolveExportTarget("./vanilla");
    const typesEntry = resolveExportTarget("./types");
    const tokens = resolveExportTarget("./tokens");
    const styles = resolveExportTarget("./styles.css");

    for (const path of [main, vanilla, typesEntry]) {
      expect(existsSync(path), `${path} should exist`).toBe(true);
    }
    expect(tokens).toBe(styles);
    expect(existsSync(tokens)).toBe(true);
    const css = readFileSync(tokens, "utf8");
    expect(css).toContain("--hearth-bg:");
    expect(css).toContain("--hearth-accent:");
    expect(css).toContain("--hearth-safe-top:");
  });

  it("main entry re-exports React components", async () => {
    const mainUrl = pathToFileURL(resolveExportTarget(".")).href;
    const mod = (await import(mainUrl)) as {
      Page: unknown;
      Button: unknown;
      Switch: unknown;
    };
    expect(mod.Page).toBeDefined();
    expect(mod.Button).toBeDefined();
    expect(mod.Switch).toBeDefined();
  });

  it("types entry exports ChromeButton shape", async () => {
    const typesUrl = pathToFileURL(resolveExportTarget("./types")).href;
    const mod = (await import(typesUrl)) as {
      ChromeButton: { kind: string };
    };
    const sample: typeof mod.ChromeButton = {
      kind: "button",
      id: "add",
      label: "Add",
      variant: "accent",
    };
    expect(sample.kind).toBe("button");
  });
});
