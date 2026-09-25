type MetricCardProps = {
  label: string;
  value: string;
  caption: string;
  icon: string;
  tone?: 'blue' | 'green' | 'amber' | 'violet';
};

export function MetricCard({
  label,
  value,
  caption,
  icon,
  tone = 'blue',
}: MetricCardProps) {
  return (
    <article className="metric-card">
      <div className={`metric-icon tone-${tone}`} aria-hidden="true">
        {icon}
      </div>
      <div className="metric-label">{label}</div>
      <div className="metric-value">{value}</div>
      <div className="metric-caption">{caption}</div>
    </article>
  );
}
