import { useState } from 'react';

import type { CaseRecord, LLMConfiguration } from './api';
import { AppShell } from './components/AppShell';
import { CaseDetailPanel } from './features/cases/CaseDetailPanel';
import { CaseQueue } from './features/cases/CaseQueue';
import { ComparisonPage } from './features/comparison/ComparisonPage';
import { InjectionDemoPage } from './features/injection/InjectionDemoPage';
import { OverviewPage } from './features/overview/OverviewPage';
import { ResultsPage } from './features/results/ResultsPage';
import { SettingsPage } from './features/settings/SettingsPage';
import { useCaseQueue } from './hooks/useCaseQueue';
import { useResults } from './hooks/useResults';
import type { AppPage } from './types';
import './styles.css';

export function App() {
  const [page, setPage] = useState<AppPage>('overview');
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);
  const [llmConfiguration, setLLMConfiguration] = useState<LLMConfiguration>({
    provider: 'fake',
    model: 'fake-model',
  });
  const casesQuery = useCaseQueue();
  const resultsQuery = useResults();
  const cases = casesQuery.data ?? [];
  const selectedCase =
    cases.find((caseItem) => caseItem.case_id === selectedCaseId) ?? cases[0] ?? null;

  function openCase(caseItem: CaseRecord) {
    setSelectedCaseId(caseItem.case_id);
    setPage('cases');
  }

  return (
    <AppShell
      activePage={page}
      configuration={llmConfiguration}
      onNavigate={setPage}
    >
      {page === 'overview' && (
        <OverviewPage
          cases={cases}
          casesLoading={casesQuery.isPending}
          casesError={casesQuery.isError ? 'Could not load the case queue.' : null}
          results={resultsQuery.data}
          resultsLoading={resultsQuery.isPending}
          resultsError={resultsQuery.isError ? 'Could not load evaluation results.' : null}
          onRetryCases={() => void casesQuery.refetch()}
          onRetryResults={() => void resultsQuery.refetch()}
          onOpenCase={openCase}
          onViewAll={() => setPage('cases')}
        />
      )}
      {page === 'cases' && (
        <div className="case-workspace">
          <CaseQueue
            cases={cases}
            loading={casesQuery.isPending}
            error={casesQuery.isError ? 'Could not load the case queue.' : null}
            selectedCaseId={selectedCase?.case_id ?? null}
            onSelect={setSelectedCaseId}
            onRetry={() => void casesQuery.refetch()}
          />
          <CaseDetailPanel caseId={selectedCase?.case_id ?? null} />
        </div>
      )}
      {page === 'results' && (
        <ResultsPage
          results={resultsQuery.data}
          loading={resultsQuery.isPending}
          error={resultsQuery.isError ? 'Could not load evaluation results.' : null}
          onRetry={() => void resultsQuery.refetch()}
        />
      )}
      {page === 'compare' && <ComparisonPage cases={cases} configuration={llmConfiguration} />}
      {page === 'injection' && (
        <InjectionDemoPage cases={cases} configuration={llmConfiguration} />
      )}
      {page === 'settings' && (
        <SettingsPage configuration={llmConfiguration} onSave={setLLMConfiguration} />
      )}
    </AppShell>
  );
}
