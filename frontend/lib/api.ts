const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function fetcher(path: string, options?: RequestInit) {
  const res = await fetch(`${API_URL}${path}`, {
    credentials: "include",
    headers: { "Content-Type": "application/json", ...options?.headers },
    ...options,
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "エラーが発生しました" }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

// Auth
export const login = (password: string) =>
  fetcher("/api/auth/login", { method: "POST", body: JSON.stringify({ password }) });

export const logout = () =>
  fetcher("/api/auth/logout", { method: "POST" });

export const getMe = () => fetcher("/api/auth/me");

// Recommend
export const recommend = (formInput: string) =>
  fetcher("/api/recommend", { method: "POST", body: JSON.stringify({ form_input: formInput }) });

// Chairs
export const getChairs = () => fetcher("/api/chairs");
export const getChair = (id: string) => fetcher(`/api/chairs/${id}`);
export const createChair = (data: Record<string, unknown>) =>
  fetcher("/api/chairs", { method: "POST", body: JSON.stringify(data) });
export const updateChair = (id: string, data: Record<string, unknown>) =>
  fetcher(`/api/chairs/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteChair = (id: string) =>
  fetcher(`/api/chairs/${id}`, { method: "DELETE" });
export const toggleRecommendable = (id: string, is_recommendable: boolean) =>
  fetcher(`/api/chairs/${id}/recommendable`, { method: "PATCH", body: JSON.stringify({ is_recommendable }) });

// Aliases
export const getAliases = (chairId: string) => fetcher(`/api/chairs/${chairId}/aliases`);
export const createAlias = (chairId: string, alias: string) =>
  fetcher(`/api/chairs/${chairId}/aliases`, { method: "POST", body: JSON.stringify({ alias }) });
export const deleteAlias = (aliasId: string) =>
  fetcher(`/api/aliases/${aliasId}`, { method: "DELETE" });

// Videos
export const getVideos = () => fetcher("/api/videos");
export const getVideo = (id: string) => fetcher(`/api/videos/${id}`);
export const syncVideos = () => fetcher("/api/videos/sync", { method: "POST" });

// Makers
export const getMakers = () => fetcher("/api/makers");
export const getMakerProducts = (maker: string) => fetcher(`/api/makers/${encodeURIComponent(maker)}/products`);
export const scrapeMakers = () => fetcher("/api/makers/scrape", { method: "POST" });
export const createScrapeConfig = (data: Record<string, unknown>) =>
  fetcher("/api/makers/configs", { method: "POST", body: JSON.stringify(data) });

// Prompts
export const getPrompts = () => fetcher("/api/prompts");
export const getPrompt = (key: string) => fetcher(`/api/prompts/${key}`);
export const updatePrompt = (key: string, content: string) =>
  fetcher(`/api/prompts/${key}`, { method: "PUT", body: JSON.stringify({ content }) });
export const getPromptVersions = (key: string) => fetcher(`/api/prompts/${key}/versions`);
export const rollbackPrompt = (key: string, version: number) =>
  fetcher(`/api/prompts/${key}/rollback/${version}`, { method: "POST" });
export const testPrompt = (key: string, sampleInput: string) =>
  fetcher(`/api/prompts/${key}/test`, { method: "POST", body: JSON.stringify({ sample_input: sampleInput }) });

// Pipeline
export const startBulkBuild = () => fetcher("/api/pipeline/bulk-build", { method: "POST" });
export const getBulkBuildStatus = () => fetcher("/api/pipeline/bulk-build/status");
export const extractVideo = (videoId: string) =>
  fetcher(`/api/pipeline/extract/${videoId}`, { method: "POST" });
export const clusterMentions = () => fetcher("/api/pipeline/cluster", { method: "POST" });

// Logs
export const getExtractionLogs = (params?: Record<string, string>) => {
  const query = params ? "?" + new URLSearchParams(params).toString() : "";
  return fetcher(`/api/logs/extraction${query}`);
};
export const getRecommendationLogs = () => fetcher("/api/logs/recommendation");
export const getUnresolvedLogs = () => fetcher("/api/extraction-logs?status=unresolved");
export const resolveLog = (logId: string, chairId: string) =>
  fetcher(`/api/extraction-logs/${logId}/resolve`, { method: "PATCH", body: JSON.stringify({ chair_id: chairId }) });
export const ignoreLog = (logId: string) =>
  fetcher(`/api/extraction-logs/${logId}/ignore`, { method: "POST" });
