import { useEffect, useState } from 'react';

export type CaseRecord = {
  case_id: string;
  merchant: string;
  amount: number;
  status: 'flagged' | 'clear';
  risk_score: number;
};

const fallbackCases: CaseRecord[] = [
  { case_id: 'case-0', merchant: 'Northwind', amount: 420.5, status: 'flagged', risk_score: 0.93 },
  { case_id: 'case-1', merchant: 'Café Bloc', amount: 95.3, status: 'clear', risk_score: 0.12 },
];

export function useCaseQueue() {
  const [cases, setCases] = useState<CaseRecord[]>(fallbackCases);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/cases')
      .then((response) => (response.ok ? response.json() : { cases: fallbackCases }))
      .then((payload) => {
        setCases(payload.cases ?? fallbackCases);
      })
      .catch(() => {
        setCases(fallbackCases);
      })
      .finally(() => setLoading(false));
  }, []);

  return { cases, loading };
}
