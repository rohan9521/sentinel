import { useMutation } from '@tanstack/react-query';
import { useEffect, useState } from 'react';

import {
  analyzeCase,
  type CaseRecord,
  type LLMConfiguration,
} from '../../api';
import { QueryState } from '../../components/QueryState';

type ComparisonPageProps = {
  cases: CaseRecord[];
  configuration: LLMConfiguration;
};

export function ComparisonPage({ cases, configuration }: ComparisonPageProps) {
  const [caseId, setCaseId] = useState(cases[0]?.case_id ?? '');
  const [memo, setMemo] = useState('');
  const selectedCase = cases.find((item) => item.case_id === caseId);
  useEffect(() => {
    if (!caseId && cases[0]) {
      setCaseId(cases[0].case_id);
    }
  }, [caseId, cases]);
  const mutation = useMutation({
    mutationFn: () => analyzeCase(caseId, memo, configuration),
  });

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Analysis / Language model</p>
          <h1>LLM case analysis</h1>
          <p className="page-description">
            Ask the selected provider to review synthetic case context. Choose and configure
            the provider in LLM settings.
          </p>
        </div>
      </div>
      <section className="panel comparison-panel">
        <div className="comparison-controls">
          <label className="form-field">
            <span>Transaction case</span>
            <select value={caseId} onChange={(event) => setCaseId(event.target.value)}>
              {cases.map((item) => (
                <option key={item.case_id} value={item.case_id}>
                  {item.case_id} · {item.merchant}
                </option>
              ))}
            </select>
          </label>
          <label className="form-field">
            <span>Untrusted payment memo</span>
            <input
              value={memo}
              onChange={(event) => setMemo(event.target.value)}
              placeholder={selectedCase ? `${selectedCase.merchant} · $${selectedCase.amount}` : 'Enter context'}
            />
          </label>
          <button
            className="button button-primary"
            type="button"
            disabled={!caseId || mutation.isPending}
            onClick={() => mutation.mutate()}
          >
            {mutation.isPending ? 'Running…' : '            Analyze case'}
          </button>
        </div>
        <div className="notice notice-warning">
          Provider: <strong>{configuration.provider}</strong> · model:{' '}
          <strong>{configuration.model}</strong>. Fake mode returns a placeholder. Hosted model
          requests may incur provider charges.
        </div>

        {mutation.isPending && <QueryState kind="loading" title="Requesting model analysis" />}
        {mutation.isError && (
          <QueryState
            kind="error"
            title="LLM request failed"
            message={mutation.error.message}
            action={() => mutation.mutate()}
          />
        )}
        {mutation.data && (
          <div className="analysis-result" aria-live="polite">
            <div className="analysis-meta">
              <span>{mutation.data.provider} · {mutation.data.model}</span>
              <span>{mutation.data.latency_ms} ms</span>
            </div>
            {mutation.data.placeholder && (
              <p className="notice notice-warning">
                This is a fake placeholder response, not a generated analysis.
              </p>
            )}
            <p className="analysis-response">{mutation.data.response}</p>
          </div>
        )}
      </section>
    </>
  );
}
