import { execSync } from "node:child_process";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import pkg from "../package.json";

const pkgRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");

describe("@kindling/mantle publish packaging", () => {
  it("npm publish --dry-run lists the package tarball contents", () => {
    const out = execSync("npm publish --dry-run --access=public --ignore-scripts 2>&1", {
      cwd: pkgRoot,
      encoding: "utf8",
      shell: "/bin/sh",
    });
    expect(out).toContain(`@kindling/mantle@${pkg.version}`);
    expect(out).toContain("dist/index.js");
    expect(out).toContain("README.md");
    expect(out).toContain("CHANGELOG.md");
  });
});
