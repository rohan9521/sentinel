import type { CaseRecord, ResultPayload } from '../../api';
import { MetricCard } from '../../components/MetricCard';
import { QueryState } from '../../components/QueryState';
import { StatusBadge } from '../../components/StatusBadge';

type OverviewPageProps = {
  cases: CaseRecord[];
  casesLoading: boolean;
  casesError: string | null;
  results: ResultPayload | undefined;
  resultsLoading: boolean;
  resultsError: string | null;
  onRetryCases: () => void;
  onRetryResults: () => void;
  onOpenCase: (caseItem: CaseRecord) => void;
  onViewAll: () => void;
};

export function OverviewPage({
  cases,
  casesLoading,
  casesError,
  results,
  resultsLoading,
  resultsError,
  onRetryCases,
  onRetryResults,
  onOpenCase,
  onViewAll,
}: OverviewPageProps) {
  const flaggedCases = cases.filter((caseItem) => caseItem.status === 'flagged');
  const metrics = results?.metrics;

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Risk operations / Overview</p>
          <h1>Fraud operations overview</h1>
          <p className="page-description">
            Review flagged activity and monitor the latest evaluation run.
          </p>
        </div>
        <button className="button button-primary" type="button" onClick={onViewAll}>
          Open case queue <span aria-hidden="true">→</span>
        </button>
      </div>

      <section className="metric-grid" aria-label="Operations summary">
        <MetricCard
          label="Flagged cases"
          value={casesLoading ? '—' : String(flaggedCases.length)}
          caption="In the current demo queue"
          icon="!"
          tone="amber"
        />
        <MetricCard
          label="Cases reviewed"
          value={casesLoading ? '—' : String(cases.length)}
          caption="Synthetic transactions"
          icon="✓"
          tone="green"
        />
        <MetricCard
          label="PR-AUC"
          value={resultsLoading ? '—' : metrics ? metrics.pr_auc.toFixed(3) : '—'}
          caption={resultsError ? 'Results unavailable' : 'From latest generated result'}
          icon="↗"
          tone="blue"
        />
        <MetricCard
          label="P50 processing"
          value={
            resultsLoading
              ? '—'
              : metrics?.latency_ms_p50 === null
                ? 'Not measured'
                : metrics
                  ? `${metrics.latency_ms_p50} ms`
                  : '—'
          }
          caption="Operational latency is not measured"
          icon="◷"
          tone="violet"
        />
      </section>

      <section className="overview-grid">
        <article className="panel overview-queue">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">Needs attention</p>
              <h2>Flagged cases</h2>
            </div>
            <button className="text-button" type="button" onClick={onViewAll}>
              View queue <span aria-hidden="true">→</span>
            </button>
          </div>
          {casesLoading ? (
            <QueryState kind="loading" title="Loading cases" />
          ) : casesError ? (
            <QueryState
              kind="error"
              title="Could not load cases"
              message={casesError}
              action={onRetryCases}
            />
          ) : flaggedCases.length === 0 ? (
            <QueryState kind="empty" title="Queue is clear" message="No flagged cases are available." />
          ) : (
            <div className="table-scroll">
              <table className="data-table">
                <thead>
                  <tr><th>Case</th><th>Merchant</th><th>Amount</th><th>Risk</th><th>Status</th></tr>
                </thead>
                <tbody>
                  {flaggedCases.slice(0, 5).map((caseItem) => (
                    <tr key={caseItem.case_id}>
                      <td>
                        <button className="table-link" type="button" onClick={() => onOpenCase(caseItem)}>
                          {caseItem.case_id}
                        </button>
                      </td>
                      <td>{caseItem.merchant}</td>
                      <td>${caseItem.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}</td>
                      <td><span className="risk-value">{(caseItem.risk_score * 100).toFixed(0)}%</span></td>
                      <td><StatusBadge status={caseItem.status} /></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </article>

        <aside className="panel status-panel">
          <p className="eyebrow">Environment</p>
          <h2>Demo workspace</h2>
          <p className="subtle-text">
            Sentinel is using seeded synthetic cases and the offline demo configuration.
          </p>
          <div className="environment-indicator">
            <span className="status-dot" />
            Synthetic demo data
          </div>
          <div className="fine-print">
            Evaluation metrics are read from the backend results artifact. They are demo outputs,
            not production performance claims.
            {resultsError && (
              <button
                className="text-button retry-link"
                type="button"
                onClick={onRetryResults}
              >
                Retry results
              </button>
            )}
          </div>
        </aside>
      </section>
    </>
  );
}
