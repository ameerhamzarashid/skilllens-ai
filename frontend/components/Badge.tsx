type BadgeProps = {
  children: React.ReactNode;
  variant?: "purple" | "green" | "neutral";
};

export function Badge({ children, variant = "purple" }: BadgeProps) {
  const styles = {
    purple: "bg-purple-50 text-purple-700 ring-purple-200",
    green: "bg-green-50 text-green-700 ring-green-200",
    neutral: "bg-gray-50 text-gray-700 ring-gray-200",
  };

  return (
    <span
      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-bold ring-1 ${styles[variant]}`}
    >
      {children}
    </span>
  );
}