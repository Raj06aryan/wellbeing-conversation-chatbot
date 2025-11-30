// check if dev or prod
export const server =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";
