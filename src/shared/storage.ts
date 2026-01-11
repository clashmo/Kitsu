/**
 * SSR-safe localStorage helpers.
 * These helpers never throw on the server and always return a fallback value.
 */
export function safeLocalStorageGet<T>(
  key: string,
  fallback: T,
  parseJson: boolean = true,
): T {
  if (typeof window === "undefined" || !window.localStorage) {
    return fallback;
  }

  try {
    const raw = window.localStorage.getItem(key);
    if (raw === null) return fallback;
    if (!parseJson) {
      return raw as unknown as T;
    }
    try {
      return JSON.parse(raw) as T;
    } catch {
      return fallback;
    }
  } catch {
    return fallback;
  }
}

export function safeLocalStorageSet<T>(key: string, value: T): boolean {
  if (typeof window === "undefined" || !window.localStorage) {
    return false;
  }

  try {
    const serialized =
      typeof value === "string" ? value : JSON.stringify(value);
    window.localStorage.setItem(key, serialized);
    return true;
  } catch {
    return false;
  }
}
