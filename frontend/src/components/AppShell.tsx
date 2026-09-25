import type { ReactNode } from 'react';

import type { LLMConfiguration } from '../api';
import type { AppPage } from '../types';

type AppShellProps = {
  activePage: AppPage;
  children: ReactNode;
  configuration: LLMConfiguration;
  onNavigate: (page: AppPage) => void;
};

const navigation: { page: AppPage; label: string; icon: string }[] = [
  { page: 'overview', label: 'Overview', icon: '▦' },
  { page: 'cases', label: 'Case queue', icon: '▤' },
  { page: 'compare', label: 'LLM analysis', icon: '⇄' },
  { page: 'injection', label: 'Injection demo', icon: '⌁' },
  { page: 'results', label: 'Evaluation results', icon: '◩' },
  { page: 'settings', label: 'LLM settings', icon: '⚙' },
];

export function AppShell({ activePage, children, configuration, onNavigate }: AppShellProps) {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <a
          className="brand"
          href="#overview"
          onClick={(event) => {
            event.preventDefault();
            onNavigate('overview');
          }}
          aria-label="Sentinel overview"
        >
          <span className="brand-mark" aria-hidden="true">
            S
          </span>
          <span>
            <strong>Sentinel</strong>
            <small>Fraud intelligence</small>
          </span>
        </a>

        <div className="nav-label">Workspace</div>
        <nav className="primary-nav" aria-label="Main navigation">
          {navigation.map((item) => (
            <button
              className={`nav-item${activePage === item.page ? ' is-active' : ''}`}
              key={item.page}
              type="button"
              aria-current={activePage === item.page ? 'page' : undefined}
              onClick={() => onNavigate(item.page)}
            >
              <span className="nav-icon" aria-hidden="true">
                {item.icon}
              </span>
              {item.label}
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <span className="status-dot" />
          <span>
            <strong>{configuration.provider} provider</strong>
            <small>
              {configuration.provider === 'anthropic' ? 'Hosted API' : 'Local/offline'}
            </small>
          </span>
        </div>
      </aside>

      <div className="main-column">
        <header className="topbar">
          <div className="breadcrumb">Risk operations <span>/</span> Sentinel</div>
          <div className="topbar-user">
            <span className="avatar" aria-hidden="true">RA</span>
            <span>Risk analyst</span>
          </div>
        </header>
        <main className="page-content">{children}</main>
      </div>
    </div>
  );
}
