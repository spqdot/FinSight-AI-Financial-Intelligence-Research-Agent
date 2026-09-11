interface MetricCardProps {
  label: string;
  value: string;
  description?: string;
}

export default function MetricCard({
  label,
  value,
  description,
}: MetricCardProps) {
  return (
    <div className="rounded-xl border border-zinc-800 bg-zinc-900 p-5">
      <p className="text-sm text-zinc-400">{label}</p>

      <p className="mt-2 text-2xl font-semibold text-white">
        {value}
      </p>

      {description && (
        <p className="mt-1 text-xs text-zinc-500">
          {description}
        </p>
      )}
    </div>
  );
}