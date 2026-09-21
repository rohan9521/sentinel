import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useEffect, useState } from 'react';

const demoCases = [
  { case_id: 'case-0', amount: 420.5, merchant: 'Northwind', status: 'flagged', risk_score: 0.93 },
  { case_id: 'case-1', amount: 95.3, merchant: 'Café Bloc', status: 'clear', risk_score: 0.12 },
];

export function App() {
  const [cases, setCases] = useState(demoCases);
  const [selectedCase, setSelectedCase] = useState(demoCases[0]);

  useEffect(() => {
    const controller = new AbortController();

    fetch('http://localhost:8000/cases', { signal: controller.signal })
      .then((response) => response.ok ? response.json() : Promise.resolve({ cases: demoCases }))
      .then((payload) => {
        if (payload?.cases?.length) {
          setCases(payload.cases);
          setSelectedCase(payload.cases[0]);
        }
      })
      .catch(() => {
        setCases(demoCases);
        setSelectedCase(demoCases[0]);
      });

    return () => controller.abort();
  }, []);

  return (
    <main style={{ fontFamily: 'sans-serif', maxWidth: 1100, margin: '0 auto', padding: 24 }}>
      <header>
        <h1>Sentinel</h1>
        <p>Explainable fraud triage in offline demo mode.</p>
      </header>

      <section style={{ display: 'grid', gridTemplateColumns: 'minmax(280px, 360px) 1fr', gap: 24 }}>
        <aside>
          <h2>Case queue</h2>
          {cases.map((caseItem) => (
            <button
              key={caseItem.case_id}
              onClick={() => setSelectedCase(caseItem)}
              style={{
                display: 'block',
                width: '100%',
                marginBottom: 8,
                padding: 12,
                textAlign: 'left',
                border: '1px solid #d0d7de',
                borderRadius: 8,
                background: selectedCase.case_id === caseItem.case_id ? '#eef6ff' : '#fff',
              }}
            >
              <strong>{caseItem.case_id}</strong>
              <div>{caseItem.merchant}</div>
              <div>${caseItem.amount}</div>
              <small>{caseItem.status} · risk {caseItem.risk_score}</small>
            </button>
          ))}
        </aside>

        <article>
          <h2>Case detail</h2>
          <div style={{ border: '1px solid #d0d7de', borderRadius: 12, padding: 16 }}>
            <p><strong>Case:</strong> {selectedCase.case_id}</p>
            <p><strong>Merchant:</strong> {selectedCase.merchant}</p>
            <p><strong>Status:</strong> {selectedCase.status}</p>
            <p><strong>Risk score:</strong> {selectedCase.risk_score}</p>
            <p><strong>Amount:</strong> ${selectedCase.amount}</p>
          </div>
          <div style={{ marginTop: 16 }}>
            <h3>Method comparison</h3>
            <ul>
              <li>GBM: escalate</li>
              <li>LLM-only: request_more_info</li>
              <li>Fixed pipeline: escalate</li>
              <li>Tool-calling agent: escalate</li>
            </ul>
          </div>
        </article>
      </section>
    </main>
  );
}
