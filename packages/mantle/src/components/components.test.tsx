import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { axe } from "vitest-axe";
import {
  Button,
  Card,
  EmptyState,
  IconButton,
  Input,
  List,
  Page,
  PageHeader,
  Section,
  Select,
  Switch,
  TextArea,
} from "./index";

const MIN_TOUCH_PX = 44;

function minTouchSize(el: HTMLElement): { w: number; h: number } {
  const s = getComputedStyle(el);
  const w = Math.max(parseFloat(s.minWidth) || 0, el.getBoundingClientRect().width);
  const h = Math.max(parseFloat(s.minHeight) || 0, el.getBoundingClientRect().height);
  return { w, h };
}

describe("@kindling/mantle base components", () => {
  it("Page renders scroll shell with safe-area class", async () => {
    const { container } = render(
      <Page>
        <p>Content</p>
      </Page>,
    );
    expect(screen.getByText("Content")).toBeInTheDocument();
    expect(container.querySelector(".mantle-page")).toBeTruthy();
    expect(await axe(container)).toHaveNoViolations();
  });

  it("PageHeader renders title, subtitle, and action slot", async () => {
    const { container } = render(
      <PageHeader title="Groceries" subtitle="3 items">
        <Button>Add</Button>
      </PageHeader>,
    );
    expect(screen.getByRole("heading", { name: "Groceries" })).toBeInTheDocument();
    expect(screen.getByText("3 items")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Add" })).toBeInTheDocument();
    expect(await axe(container)).toHaveNoViolations();
  });

  it("Card and Section render grouped content", async () => {
    const { container } = render(
      <Section title="Details">
        <Card>
          <p>Inside card</p>
        </Card>
      </Section>,
    );
    expect(screen.getByText("Details")).toBeInTheDocument();
    expect(screen.getByText("Inside card")).toBeInTheDocument();
    expect(await axe(container)).toHaveNoViolations();
  });

  it("List renders items", async () => {
    const { container } = render(
      <List>
        <li>Milk</li>
        <li>Eggs</li>
      </List>,
    );
    expect(screen.getByText("Milk")).toBeInTheDocument();
    expect(await axe(container)).toHaveNoViolations();
  });

  it("EmptyState renders title, body, and action", async () => {
    const { container } = render(
      <EmptyState
        title="Nothing here"
        body="Add your first item."
        action={<Button>Get started</Button>}
      />,
    );
    expect(screen.getByRole("status")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Get started" })).toBeInTheDocument();
    expect(await axe(container)).toHaveNoViolations();
  });

  it("Button variants apply classes and meet 44px touch target", async () => {
    const { container, rerender } = render(<Button>Default</Button>);
    let btn = screen.getByRole("button", { name: "Default" });
    expect(btn.className).toContain("mantle-btn");
    let size = minTouchSize(btn);
    expect(size.w).toBeGreaterThanOrEqual(MIN_TOUCH_PX);
    expect(size.h).toBeGreaterThanOrEqual(MIN_TOUCH_PX);
    expect(await axe(container)).toHaveNoViolations();

    rerender(<Button variant="accent">Accent</Button>);
    btn = screen.getByRole("button", { name: "Accent" });
    expect(btn.className).toContain("mantle-btn--accent");

    rerender(<Button variant="ghost">Ghost</Button>);
    btn = screen.getByRole("button", { name: "Ghost" });
    expect(btn.className).toContain("mantle-btn--ghost");

    rerender(<Button variant="danger">Danger</Button>);
    btn = screen.getByRole("button", { name: "Danger" });
    expect(btn.className).toContain("mantle-btn--danger");
  });

  it("IconButton requires aria-label and meets touch target", async () => {
    const { container } = render(
      <IconButton aria-label="Add item">
        <span aria-hidden="true">+</span>
      </IconButton>,
    );
    const btn = screen.getByRole("button", { name: "Add item" });
    const size = minTouchSize(btn);
    expect(size.w).toBeGreaterThanOrEqual(MIN_TOUCH_PX);
    expect(size.h).toBeGreaterThanOrEqual(MIN_TOUCH_PX);
    expect(await axe(container)).toHaveNoViolations();
  });

  it("Input associates label and error", async () => {
    const { container } = render(
      <Input label="Email" error="Invalid email" defaultValue="bad@" />,
    );
    const input = screen.getByLabelText("Email");
    expect(input).toHaveAttribute("aria-invalid", "true");
    expect(screen.getByRole("alert")).toHaveTextContent("Invalid email");
    expect(await axe(container)).toHaveNoViolations();
  });

  it("TextArea renders with label", async () => {
    const { container } = render(<TextArea label="Notes" defaultValue="Hello" />);
    expect(screen.getByLabelText("Notes")).toHaveValue("Hello");
    expect(await axe(container)).toHaveNoViolations();
  });

  it("Select renders options", async () => {
    const { container } = render(
      <Select
        label="Theme"
        options={[
          { value: "light", label: "Light" },
          { value: "dark", label: "Dark" },
        ]}
        defaultValue="dark"
      />,
    );
    expect(screen.getByLabelText("Theme")).toHaveValue("dark");
    expect(await axe(container)).toHaveNoViolations();
  });

  it("Switch toggles with role=switch", async () => {
    const user = userEvent.setup();
    const { container } = render(<Switch label="Notifications" />);
    const sw = screen.getByRole("switch", { name: "Notifications" });
    expect(sw).not.toBeChecked();
    await user.click(sw);
    expect(sw).toBeChecked();
    const size = minTouchSize(sw.closest("label")!);
    expect(size.h).toBeGreaterThanOrEqual(MIN_TOUCH_PX);
    expect(await axe(container)).toHaveNoViolations();
  });
});
