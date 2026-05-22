import "@testing-library/jest-dom/vitest";
import * as matchers from "vitest-axe/matchers";
import { expect } from "vitest";
import "./tokens.css";
import "./components.css";

expect.extend(matchers);
