// Spark hub proxy is deferred to a later FR; v0 reports unavailable.

export interface SparkHandle {
  readonly available: false;
}

const SPARK_STUB: SparkHandle = { available: false };

export function useSpark(): SparkHandle {
  return SPARK_STUB;
}
