/**
 * Spark v1 browser client — communicates with the Hub Spark proxy endpoint.
 *
 * Authority: docs/design/spark-api.md
 *
 * Phase 1 (this file): thin stub that exposes the call/publish/subscribe
 * surface so plugin UIs can import it. The actual transport (WebSocket → broker
 * proxy) is wired up in Phase 2 when the Hub exposes a WS endpoint.
 *
 * DESIGN-GAP: Hub WS proxy for browser↔broker not yet specced. This stub
 * throws at runtime until that proxy exists. Plugin code can import the types
 * and interface now.
 */

export interface SparkCallOptions {
  timeoutMs?: number;
}

export interface SparkEventFrame {
  kind: "event";
  topic: string;
  from: string;
  payload?: Record<string, unknown>;
  ts: number;
}

export type SparkEventHandler = (frame: SparkEventFrame) => void | Promise<void>;

export interface ISparkClient {
  call(
    target: string,
    method: string,
    params?: Record<string, unknown>,
    opts?: SparkCallOptions,
  ): Promise<unknown>;
  publish(topic: string, payload?: Record<string, unknown>): Promise<void>;
  subscribe(topicPattern: string, handler: SparkEventHandler): Promise<void>;
  close(): void;
}

export class SparkNotAvailableError extends Error {
  constructor() {
    super("Spark browser client is not yet available — Hub WS proxy not implemented (Phase 2).");
    this.name = "SparkNotAvailableError";
  }
}

/**
 * Stub implementation. Import and wire up in plugin UI code; replace with the
 * real WS-backed implementation once the Hub proxy lands.
 */
export class SparkClient implements ISparkClient {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async call(_target: string, _method: string, _params?: Record<string, unknown>): Promise<unknown> {
    throw new SparkNotAvailableError();
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async publish(_topic: string, _payload?: Record<string, unknown>): Promise<void> {
    throw new SparkNotAvailableError();
  }

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  async subscribe(_topicPattern: string, _handler: SparkEventHandler): Promise<void> {
    throw new SparkNotAvailableError();
  }

  close(): void {
    // no-op for stub
  }
}

export const sparkClient: ISparkClient = new SparkClient();
