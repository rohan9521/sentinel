import { useMemo, useState } from 'react';

import type { CaseRecord } from '../../api';
import { QueryState } from '../../components/QueryState';
import { StatusBadge } from '../../components/StatusBadge';

type CaseQueueProps = {
  cases: CaseRecord[];
  loading: boolean;
  error: string | null;
  selectedCaseId: string | null;
  onSelect: (caseId: string) => void;
  onRetry: () => void;
};

type CaseFilter = 'all' | 'flagged' | 'clear';

const filters: { value: CaseFilter; label: string }[] = [
  { value: 'all', label: 'All cases' },
  { value: 'flagged', label: 'Flagged' },
  { value: 'clear', label: 'Cleared' },
];

export function CaseQueue({
  cases,
  loading,
  error,
  selectedCaseId,
  onSelect,
  onRetry,
}: CaseQueueProps) {
  const [filter, setFilter] = useState<CaseFilter>('all');
  const [search, setSearch] = useState('');
  const visibleCases = useMemo(
    () =>
      cases.filter((caseItem) => {
        const matchesFilter = filter === 'all' || caseItem.status === filter;
        const searchValue = `${caseItem.case_id} ${caseItem.merchant} ${caseItem.account_id}`;
        return matchesFilter && searchValue.toLowerCase().includes(search.toLowerCase());
      }),
    [cases, filter, search],
  );

  return (
    <section className="panel queue-panel" aria-labelledby="queue-heading">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Investigations</p>
          <h2 id="queue-heading">Case queue</h2>
        </div>
        <span className="count-pill">{cases.length}</span>
      </div>
      <label className="search-field">
        <span className="sr-only">Search cases</span>
        <span aria-hidden="true">⌕</span>
        <input
          type="search"
          placeholder="Search cases or accounts"
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
      </label>
      <div className="filter-tabs" role="group" aria-label="Filter case queue">
        {filters.map((item) => (
          <button
            className={filter === item.value ? 'filter-tab is-selected' : 'filter-tab'}
            key={item.value}
            type="button"
            aria-pressed={filter === item.value}
            onClick={() => setFilter(item.value)}
          >
            {item.label}
          </button>
        ))}
      </div>

      {loading ? (
        <QueryState kind="loading" title="Loading cases" message="Fetching the latest queue." />
      ) : error ? (
        <QueryState kind="error" title="Queue unavailable" message={error} action={onRetry} />
      ) : visibleCases.length === 0 ? (
        <QueryState
          kind="empty"
          title="No matching cases"
          message="Try another search or status filter."
        />
      ) : (
        <ul className="case-list">
          {visibleCases.map((caseItem) => (
            <li key={caseItem.case_id}>
              <button
                className={`case-row${selectedCaseId === caseItem.case_id ? ' is-selected' : ''}`}
                type="button"
                onClick={() => onSelect(caseItem.case_id)}
                aria-pressed={selectedCaseId === caseItem.case_id}
              >
                <span className="case-row-top">
                  <strong>{caseItem.case_id}</strong>
                  <StatusBadge status={caseItem.status} />
                </span>
                <span className="case-row-merchant">{caseItem.merchant}</span>
                <span className="case-row-bottom">
                  <span>{caseItem.account_id}</span>
                  <span>${caseItem.amount.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span>
                </span>
                <span className="risk-track" aria-label={`Risk score ${(caseItem.risk_score * 100).toFixed(0)} percent`}>
                  <span style={{ width: `${Math.max(0, Math.min(100, caseItem.risk_score * 100))}%` }} />
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
