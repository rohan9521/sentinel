import { useCaseQueue } from './hooks/useCaseQueue';

export function App() {
  const { cases, loading } = useCaseQueue();
  const selectedCase = cases[0] ?? {
    case_id: 'none',
    merchant: 'No cases',
    amount: 0,
    status: 'clear',
    risk_score: 0,
  };

  return (
    <main style={{ fontFamily: 'sans-serif', maxWidth: 1100, margin: '0 auto', padding: 24 }}>
      <header>
        <h1>Sentinel</h1>
        <p>Explainable fraud triage in offline demo mode.</p>
      </header>

      <section style={{ display: 'grid', gridTemplateColumns: 'minmax(280px, 360px) 1fr', gap: 24 }}>
        <aside>
          <h2>Case queue</h2>
          {loading ? <p>Loading cases…</p> : cases.map((caseItem) => (
            <button
              key={caseItem.case_id}
              style={{
                display: 'block',
                width: '100%',
                marginBottom: 8,
                padding: 12,
                textAlign: 'left',
                border: '1px solid #d0d7de',
                borderRadius: 8,
                background: '#fff',
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
