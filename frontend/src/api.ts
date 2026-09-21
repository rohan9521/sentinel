import { describe, expect, it } from 'vitest';

export type CaseRecord = {
  case_id: string;
  merchant: string;
  amount: number;
  status: 'flagged' | 'clear';
  risk_score: number;
};

export function fetchCases() {
  return Promise.resolve([
    { case_id: 'case-0', merchant: 'Northwind', amount: 420.5, status: 'flagged', risk_score: 0.93 },
    { case_id: 'case-1', merchant: 'Café Bloc', amount: 95.3, status: 'clear', risk_score: 0.12 },
  ] as CaseRecord[]);
}

describe('fetchCases', () => {
  it('returns the demo queue', async () => {
    const cases = await fetchCases();
    expect(cases.length).toBeGreaterThan(0);
    expect(cases[0].status).toBe('flagged');
  });
});
