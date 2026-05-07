import { ReactNode } from "react";

type StatCardProps = {
  label: string;
  value: string | number;
  icon?: ReactNode;
  hint?: string;
};

export function StatCard({ label, value, icon, hint }: StatCardProps) {
  return (
    <div className="card-shadow soft-border rounded-[1.4rem] bg-white p-5">
      <div className="mb-4 flex items-center justify-between">
        <div className="text-sm font-bold uppercase tracking-wide text-gray-500">
          {label}
        </div>
        {icon ? (
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-100 to-green-100 text-purple-700">
            {icon}
          </div>
        ) : null}
      </div>
      <div className="text-3xl font-black tracking-tight text-purple-700">
        {value}
      </div>
      {hint ? <div className="mt-2 text-sm text-gray-500">{hint}</div> : null}
    </div>
  );
}