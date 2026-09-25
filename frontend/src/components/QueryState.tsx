type QueryStateProps = {
  title: string;
  message?: string;
  kind: 'loading' | 'error' | 'empty';
  action?: () => void;
};

export function QueryState({ title, message, kind, action }: QueryStateProps) {
  return (
    <div className={`query-state query-state-${kind}`} role={kind === 'error' ? 'alert' : 'status'}>
      {kind === 'loading' && <span className="spinner" aria-hidden="true" />}
      {kind === 'error' && <span className="state-symbol" aria-hidden="true">!</span>}
      {kind === 'empty' && <span className="state-symbol" aria-hidden="true">—</span>}
      <strong>{title}</strong>
      {message && <p>{message}</p>}
      {action && (
        <button className="button button-secondary" type="button" onClick={action}>
          Try again
        </button>
      )}
    </div>
  );
}
