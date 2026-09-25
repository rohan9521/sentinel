import { useState, type FormEvent } from 'react';

import type { LLMConfiguration, LLMProvider } from '../../api';

type SettingsPageProps = {
  configuration: LLMConfiguration;
  onSave: (configuration: LLMConfiguration) => void;
};

const providerDefaults: Record<LLMProvider, string> = {
  fake: 'fake-model',
  anthropic: 'claude-3-5-haiku-latest',
  ollama: 'qwen2.5:3b',
};

function isLLMProvider(value: string): value is LLMProvider {
  return value === 'fake' || value === 'anthropic' || value === 'ollama';
}

export function SettingsPage({ configuration, onSave }: SettingsPageProps) {
  const [provider, setProvider] = useState<LLMProvider>(configuration.provider);
  const [model, setModel] = useState(configuration.model);
  const [apiKey, setApiKey] = useState(configuration.apiKey ?? '');
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<string | null>(null);

  function selectProvider(nextProvider: LLMProvider) {
    setProvider(nextProvider);
    setModel(providerDefaults[nextProvider]);
    if (nextProvider !== 'anthropic') {
      setApiKey('');
    }
    setSaved(false);
    setError(null);
  }

  function saveSettings(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (provider === 'anthropic' && !apiKey.trim()) {
      setError('Enter an Anthropic API key to use the hosted model.');
      setSaved(false);
      return;
    }
    const nextConfiguration: LLMConfiguration = {
      provider,
      model: model.trim(),
      ...(provider === 'anthropic' ? { apiKey: apiKey.trim() } : {}),
    };
    onSave(nextConfiguration);
    setSaved(true);
    setError(null);
  }

  return (
    <>
      <div className="page-heading">
        <div>
          <p className="eyebrow">Workspace / Configuration</p>
          <h1>Language model</h1>
          <p className="page-description">
            Choose a hosted Anthropic model, local Ollama, or the no-cost fake demo.
          </p>
        </div>
      </div>
      <form className="panel settings-panel" onSubmit={saveSettings}>
        <label className="form-field">
          <span>Provider</span>
          <select
            value={provider}
            onChange={(event) => {
              if (isLLMProvider(event.target.value)) {
                selectProvider(event.target.value);
              }
            }}
          >
            <option value="fake">Fake LLM · offline demo</option>
            <option value="anthropic">Anthropic · API key required</option>
            <option value="ollama">Ollama · local inference</option>
          </select>
        </label>

        <label className="form-field">
          <span>Model name</span>
          <input
            required
            value={model}
            onChange={(event) => {
              setModel(event.target.value);
              setSaved(false);
            }}
            placeholder={providerDefaults[provider]}
          />
        </label>

        {provider === 'anthropic' && (
          <label className="form-field">
            <span>Anthropic API key</span>
            <input
              type="password"
              autoComplete="off"
              value={apiKey}
              onChange={(event) => {
                setApiKey(event.target.value);
                setSaved(false);
              }}
              placeholder="sk-ant-…"
            />
          </label>
        )}

        {provider === 'ollama' && (
          <div className="provider-help">
            <strong>Use a local Ollama model</strong>
            <p>
              Install and start Ollama, then download a model, for example{' '}
              <code>ollama pull qwen2.5:3b</code>. Sentinel connects to{' '}
              <code>http://127.0.0.1:11434</code> by default. To use a different local endpoint,
              set <code>SENTINEL_OLLAMA_BASE_URL</code> in the backend environment.
            </p>
          </div>
        )}

        {provider === 'fake' && (
          <div className="provider-help">
            Fake mode makes no model-provider request and requires no credentials. Its response
            is a placeholder, not an actual fraud assessment.
          </div>
        )}

        <div className="secret-notice">
          {provider === 'anthropic'
            ? 'The API key is kept only in this page session, sent to the local backend for each request, and is not saved to browser storage.'
            : 'Provider choice is kept in this page session; no API credentials are sent.'}
        </div>

        {error && <p className="form-error" role="alert">{error}</p>}
        {saved && <p className="form-success" role="status">Provider settings applied for this session.</p>}
        <button className="button button-primary" type="submit">
          Apply settings
        </button>
      </form>
    </>
  );
}
