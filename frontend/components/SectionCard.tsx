import { ReactNode } from "react";

type SectionCardProps = {
  title: string;
  description?: string;
  children: ReactNode;
};

export function SectionCard({ title, description, children }: SectionCardProps) {
  return (
    <section className="card-shadow soft-border rounded-[1.6rem] bg-white p-6">
      <div className="mb-5">
        <h2 className="text-xl font-black tracking-tight text-gray-950">
          {title}
        </h2>
        {description ? (
          <p className="mt-1 text-sm leading-6 text-gray-500">{description}</p>
        ) : null}
      </div>
      {children}
    </section>
  );
}