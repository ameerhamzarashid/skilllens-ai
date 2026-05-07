import Link from "next/link";
import { ArrowRight, BarChart3, BrainCircuit, BriefcaseBusiness, Compass, Database, Network, PoundSterling } from "lucide-react";
import { SectionCard } from "@/components/SectionCard";

const features = [
  {
    title: "Market Intelligence",
    description: "Explore job demand, salaries, role categories and workforce trends.",
    href: "/market",
    icon: BarChart3,
  },
  {
    title: "CV Job Matcher",
    description: "Paste CV text and rank job postings using skill-based matching.",
    href: "/cv-match",
    icon: BriefcaseBusiness,
  },
  {
    title: "Salary Predictor",
    description: "Estimate salary ranges using the trained ML regression model.",
    href: "/salary",
    icon: PoundSterling,
  },
  {
    title: "Skill Gap Roadmap",
    description: "Find missing skills and generate a personalised learning plan.",
    href: "/skill-gap",
    icon: Compass,
  },
];

const stack = [
  "Python",
  "FastAPI",
  "PostgreSQL",
  "SQLAlchemy",
  "Machine Learning",
  "Next.js",
  "TypeScript",
  "Tailwind CSS",
  "Plotly",
  "Recharts",
];

export default function HomePage() {
  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <section className="grid items-center gap-10 lg:grid-cols-[1.1fr_0.9fr]">
        <div>
          <div className="mb-5 inline-flex rounded-full border border-purple-200 bg-white px-4 py-2 text-sm font-bold text-purple-700 shadow-sm">
            Full-stack data and AI platform
          </div>

          <h1 className="max-w-4xl text-5xl font-black tracking-tight text-gray-950 md:text-6xl">
            SkillLens AI
            <span className="gradient-text block">
              Workforce Intelligence Platform
            </span>
          </h1>

          <p className="mt-6 max-w-2xl text-lg leading-8 text-gray-600">
            Analyse job market demand, discover high-value skills, match CVs to
            job postings, predict salary ranges and generate personalised career
            roadmaps using a full-stack data and AI system.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <Link href="/market" className="btn-primary">
              Open Dashboard
            </Link>
            <Link href="/cv-match" className="btn-secondary">
              Try CV Match
            </Link>
          </div>
        </div>

        <div className="card-shadow soft-border rounded-[2rem] bg-white p-6">
          <div className="mb-6 flex items-center gap-3">
            <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-700 to-green-500 text-white">
              <BrainCircuit />
            </div>
            <div>
              <div className="text-lg font-black text-gray-950">
                Platform Architecture
              </div>
              <div className="text-sm text-gray-500">
                Data engineering to frontend delivery
              </div>
            </div>
          </div>

          <div className="space-y-3">
            {[
              ["Data Platform", "Generate, clean and ingest job postings"],
              ["Database Layer", "SQLAlchemy with SQLite/PostgreSQL readiness"],
              ["ML Intelligence", "Salary prediction and CV-job matching"],
              ["FastAPI Backend", "Service layer, schemas and REST endpoints"],
              ["Next.js Frontend", "Modern TypeScript user interface"],
            ].map(([title, description]) => (
              <div
                key={title}
                className="rounded-2xl border border-gray-200 bg-gray-50 p-4"
              >
                <div className="font-black text-gray-950">{title}</div>
                <div className="mt-1 text-sm text-gray-500">{description}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-4">
        {features.map((feature) => {
          const Icon = feature.icon;

          return (
            <Link
              href={feature.href}
              key={feature.title}
              className="card-shadow soft-border rounded-[1.6rem] bg-white p-6 transition hover:-translate-y-1 hover:border-purple-300"
            >
              <div className="mb-5 flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-100 to-green-100 text-purple-700">
                <Icon />
              </div>
              <h2 className="text-lg font-black text-gray-950">
                {feature.title}
              </h2>
              <p className="mt-2 text-sm leading-6 text-gray-500">
                {feature.description}
              </p>
              <div className="mt-4 flex items-center gap-2 text-sm font-black text-purple-700">
                Explore <ArrowRight size={16} />
              </div>
            </Link>
          );
        })}
      </section>

      <section className="mt-14 grid gap-6 lg:grid-cols-2">
        <SectionCard
          title="What this project proves"
          description="A flagship portfolio project showing skills beyond Python notebooks."
        >
          <div className="grid gap-3 sm:grid-cols-2">
            {[
              "Data Engineering",
              "Analytics Engineering",
              "Machine Learning",
              "Backend APIs",
              "System Design",
              "Databases",
              "Full-stack UI",
              "Testing",
            ].map((item) => (
              <div
                key={item}
                className="rounded-2xl border border-gray-200 bg-gray-50 px-4 py-3 font-bold text-gray-700"
              >
                {item}
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard
          title="Technology stack"
          description="Modern tools used across the full system."
        >
          <div className="flex flex-wrap gap-3">
            {stack.map((item) => (
              <span
                key={item}
                className="rounded-full bg-gradient-to-r from-purple-50 to-green-50 px-4 py-2 text-sm font-black text-gray-700 ring-1 ring-gray-200"
              >
                {item}
              </span>
            ))}
          </div>
        </SectionCard>
      </section>
    </main>
  );
}