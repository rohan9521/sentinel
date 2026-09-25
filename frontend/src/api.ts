export type CaseRecord = {
  case_id: string;
  account_id: string;
  merchant: string;
  amount: number;
  status: 'flagged' | 'clear';
  risk_score: number;
  timestamp: string;
};

export type EvidenceRecord = {
  source: string;
  detail: string;
};

export type CaseDetail = CaseRecord & {
  currency: string;
  channel: string;
  memo: string;
  evidence: EvidenceRecord[];
};

export type ResultMetrics = {
  pr_auc: number;
  recall_at_precision_90: number;
  latency_ms_p50: number | null;
  latency_ms_p95: number | null;
  usd_per_case: number | null;
};

export type ResultPayload = {
  metrics: ResultMetrics;
  generated_at: number | string;
};

export type LLMProvider = 'fake' | 'anthropic' | 'ollama';

export type LLMConfiguration = {
  provider: LLMProvider;
  model: string;
  apiKey?: string;
};

export type LLMAnalysisResponse = {
  case_id: string;
  provider: LLMProvider;
  model: string;
  response: string;
  latency_ms: number;
  offline: boolean;
  placeholder: boolean;
};

const API_BASE = '/api';

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL ?? API_BASE}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function fetchCases(): Promise<CaseRecord[]> {
  const payload = await fetchJson<{ cases: CaseRecord[] }>('/cases');
  return payload.cases;
}

export async function fetchCase(caseId: string): Promise<CaseDetail> {
  return fetchJson<CaseDetail>(`/cases/${encodeURIComponent(caseId)}`);
}

export async function fetchResults(): Promise<ResultPayload> {
  return fetchJson<ResultPayload>('/results');
}

export async function analyzeCase(
  caseId: string,
  memo: string,
  config: LLMConfiguration,
): Promise<LLMAnalysisResponse> {
  const response = await fetch(`${import.meta.env.VITE_API_BASE_URL ?? API_BASE}/compare`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      case_id: caseId,
      memo,
      provider: config.provider,
      model: config.model,
      ...(config.provider === 'anthropic' ? { api_key: config.apiKey } : {}),
    }),
  });
  if (!response.ok) {
    const error = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(error?.detail ?? `LLM request failed: ${response.status}`);
  }
  return response.json() as Promise<LLMAnalysisResponse>;
}
