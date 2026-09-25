import type { ResultPayload } from '../../api';
import { MetricCard } from '../../components/MetricCard';
import { QueryState } from '../../components/QueryState';

type ResultsPageProps = {
  results: ResultPayload | undefined;
  loading: boolean;
  error: string | null;
  onRetry: () => void;
};

export function ResultsPage({ results, loading, error, onRetry }: ResultsPageProps) {
  if (loading) {
    return <QueryState kind="loading" title="Loading evaluation results" />;
  }
  if (error || !results) {
    return (
      <QueryState
        kind="error"
        title="Results unavailable"
        message={error ?? 'The backend did not return a results artifact.'}
        action={onRetry}
      />
    );
  }

  const { metrics } = results;
  const generatedAt =
    typeof results.generated_at === 'number'
      ? new Date(results.generated_at * 1000).toLocaleString()
      : results.generated_at;

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Evaluation / Results</p>
          <h1>Baseline evaluation</h1>
          <p className="page-description">
            Metrics served by the backend from the generated evaluation artifact.
          </p>
        </div>
        <span className="artifact-tag">Generated {generatedAt}</span>
      </div>

      <section className="metric-grid" aria-label="Evaluation metrics">
        <MetricCard label="PR-AUC" value={metrics.pr_auc.toFixed(3)} caption="Precision-recall area" icon="↗" />
        <MetricCard
          label="Recall at 90% precision"
          value={metrics.recall_at_precision_90.toFixed(3)}
          caption="Best recall meeting precision target"
          icon="◎"
          tone="green"
        />
        <MetricCard
          label="Median latency"
          value={metrics.latency_ms_p50 === null ? 'Not measured' : `${metrics.latency_ms_p50} ms`}
          caption="P50 runtime measurement unavailable"
          icon="◷"
          tone="violet"
        />
        <MetricCard
          label="P95 latency"
          value={metrics.latency_ms_p95 === null ? 'Not measured' : `${metrics.latency_ms_p95} ms`}
          caption="P95 runtime measurement unavailable"
          icon="◴"
          tone="amber"
        />
        <MetricCard
          label="Cost per case"
          value={metrics.usd_per_case === null ? 'Not measured' : `$${metrics.usd_per_case.toFixed(4)}`}
          caption="Cost measurement unavailable"
          icon="$"
        />
      </section>

      <section className="panel methodology-panel">
        <div>
          <p className="eyebrow">How to interpret this</p>
          <h2>Prototype results, not a production benchmark</h2>
          <p>
            This demo currently reports a single seeded baseline run. Latency and cost are
            explicitly unavailable because they are not measured from live requests. The
            detection metrics use synthetic data and are not production performance claims.
          </p>
        </div>
        <div className="artifact-path">
          <span aria-hidden="true">▧</span>
          <code>results/baseline_demo.json</code>
        </div>
      </section>
    </>
  );
}
