/* eslint-disable @typescript-eslint/no-explicit-any */
export function normalizeToJson(input: string): any {
  try {
    // 1. Try standard JSON first
    return JSON.parse(input);
  } catch {
    // 2. Convert "key: value" → proper JSON
    const obj: Record<string, any> = {};
    const lines = input.split("\n");

    for (const line of lines) {
      if (!line.includes(":")) continue;

      const [key, ...rest] = line.split(":");
      const value = rest.join(":").trim();

      // convert numbers, booleans automatically
      let parsedValue: any = value;

      if (!isNaN(Number(value))) parsedValue = Number(value);
      if (value === "true") parsedValue = true;
      if (value === "false") parsedValue = false;

      // remove surrounding quotes
      parsedValue = parsedValue.replace?.(/^"(.*)"$/, "$1");

      obj[key.trim()] = parsedValue;
    }

    return obj;
  }
}
