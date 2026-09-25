import { useQuery } from '@tanstack/react-query';

import { fetchCase } from '../../api';
import { QueryState } from '../../components/QueryState';
import { StatusBadge } from '../../components/StatusBadge';

type CaseDetailPanelProps = {
  caseId: string | null;
};

export function CaseDetailPanel({ caseId }: CaseDetailPanelProps) {
  const query = useQuery({
    queryKey: ['case', caseId],
    queryFn: () => fetchCase(caseId ?? ''),
    enabled: caseId !== null,
    retry: 1,
  });

  if (!caseId) {
    return (
      <section className="panel detail-panel">
        <QueryState kind="empty" title="Select a case" message="Choose a case from the queue to inspect its details." />
      </section>
    );
  }

  if (query.isPending) {
    return (
      <section className="panel detail-panel">
        <QueryState kind="loading" title="Loading case" message={`Fetching ${caseId}.`} />
      </section>
    );
  }

  if (query.isError) {
    return (
      <section className="panel detail-panel">
        <QueryState
          kind="error"
          title="Case details unavailable"
          message="The API could not return this case."
          action={() => void query.refetch()}
        />
      </section>
    );
  }

  const caseItem = query.data;
  return (
    <article className="panel detail-panel">
      <div className="detail-heading">
        <div>
          <p className="eyebrow">Transaction review</p>
          <h2>{caseItem.case_id}</h2>
        </div>
        <StatusBadge status={caseItem.status} />
      </div>

      <section className="risk-summary" aria-label="Risk summary">
        <div className="risk-score">{(caseItem.risk_score * 100).toFixed(0)}<small>/100</small></div>
        <div>
          <strong>Risk score</strong>
          <p>Model assessment for this synthetic transaction</p>
        </div>
        <div className="risk-track risk-track-large">
          <span style={{ width: `${Math.max(0, Math.min(100, caseItem.risk_score * 100))}%` }} />
        </div>
      </section>

      <section className="detail-section">
        <div className="section-heading">
          <h3>Transaction</h3>
          <span className="subtle-text">
            {new Date(caseItem.timestamp).toLocaleString()}
          </span>
        </div>
        <dl className="detail-grid">
          <div><dt>Amount</dt><dd>{caseItem.currency} {caseItem.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}</dd></div>
          <div><dt>Merchant</dt><dd>{caseItem.merchant}</dd></div>
          <div><dt>Account</dt><dd>{caseItem.account_id}</dd></div>
          <div><dt>Channel</dt><dd className="capitalize">{caseItem.channel}</dd></div>
        </dl>
        <div className="memo-card">
          <span className="eyebrow">Payment memo</span>
          <p>{caseItem.memo}</p>
        </div>
      </section>

      <section className="detail-section">
        <div className="section-heading">
          <div>
            <h3>Evidence</h3>
            <p className="subtle-text">Signals attached to the demo case</p>
          </div>
          <span className="count-pill">{caseItem.evidence.length}</span>
        </div>
        {caseItem.evidence.length === 0 ? (
          <QueryState kind="empty" title="No evidence available" />
        ) : (
          <ul className="evidence-list">
            {caseItem.evidence.map((evidence, index) => (
              <li key={`${evidence.source}-${index}`}>
                <span className="evidence-icon" aria-hidden="true">✓</span>
                <div>
                  <span className="evidence-source">{evidence.source}</span>
                  <p>{evidence.detail}</p>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>
    </article>
  );
}
