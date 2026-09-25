type StatusBadgeProps = {
  status: 'flagged' | 'clear';
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const label = status === 'flagged' ? 'Flagged' : 'Cleared';
  return <span className={`status-badge status-${status}`}>{label}</span>;
}
