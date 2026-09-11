interface HealthBadgeProps {
  label: string;
  value: string;
}

export default function HealthBadge({
  label,
  value,
}: HealthBadgeProps) {
  const normalizedValue = value.toLowerCase();

  const isStrong =
    normalizedValue.includes("strong") ||
    normalizedValue.includes("low");

  const isModerate =
    normalizedValue.includes("moderate") ||
    normalizedValue.includes("adequate");

  const badgeClass = isStrong
    ? "border-green-800 bg-green-950 text-green-400"
    : isModerate
      ? "border-yellow-800 bg-yellow-950 text-yellow-400"
      : "border-red-800 bg-red-950 text-red-400";

  return (
    <div className="flex items-center justify-between border-b border-zinc-800 py-3 last:border-b-0">
      <span className="text-sm text-zinc-400">{label}</span>

      <span
        className={`rounded-full border px-3 py-1 text-xs font-medium ${badgeClass}`}
      >
        {value}
      </span>
    </div>
  );
}