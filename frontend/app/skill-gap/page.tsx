"use client";

import { useState } from "react";
import { analyseSkillGap } from "@/lib/api";
import { SkillGapResponse } from "@/lib/types";
import { SectionCard } from "@/components/SectionCard";
import { Badge } from "@/components/Badge";

const exampleCv = `Data Analyst and Data Scientist with Python, SQL, Excel, Power BI, Pandas, NumPy, machine learning, Tableau and PostgreSQL experience.`;

export default function SkillGapPage() {
  const [cvText, setCvText] = useState(exampleCv);
  const [result, setResult] = useState<SkillGapResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleAnalyse() {
    setLoading(true);
    setError("");

    try {
      const data = await analyseSkillGap(cvText, 10);
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Skill gap analysis failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <div className="mb-10">
        <h1 className="text-4xl font-black tracking-tight text-gray-950">
          Skill Gap Roadmap
        </h1>
        <p className="mt-3 max-w-2xl text-gray-600">
          Compare CV skills against market demand and generate a personalised
          learning roadmap.
        </p>
      </div>

      <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Paste CV Text">
          <textarea
            className="input-style min-h-72"
            value={cvText}
            onChange={(event) => setCvText(event.target.value)}
          />

          <button className="btn-primary mt-5" onClick={handleAnalyse}>
            {loading ? "Analysing..." : "Analyse Skill Gap"}
          </button>

          {error ? (
            <div className="mt-5 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm font-semibold text-red-700">
              {error}
            </div>
          ) : null}
        </SectionCard>

        <SectionCard title="Missing Skill Priorities">
          {!result ? (
            <div className="rounded-2xl bg-gray-50 p-5 text-gray-500">
              Run the analysis to see missing skills.
            </div>
          ) : result.missing_skills.length === 0 ? (
            <div className="rounded-2xl bg-green-50 p-5 font-bold text-green-700">
              No major missing skills found.
            </div>
          ) : (
            <div className="space-y-3">
              {result.missing_skills.map((item, index) => (
                <div
                  key={item.skill}
                  className="flex items-center justify-between rounded-2xl border border-gray-200 bg-gray-50 px-4 py-3"
                >
                  <div className="font-black text-gray-800">
                    {index + 1}. {item.skill}
                  </div>
                  <Badge variant={index < 3 ? "purple" : "green"}>
                    {item.missing_count} jobs
                  </Badge>
                </div>
              ))}
            </div>
          )}
        </SectionCard>
      </section>

      <section className="mt-8">
        <SectionCard title="Personalised Learning Roadmap">
          {!result ? (
            <div className="rounded-2xl bg-gray-50 p-5 text-gray-500">
              No roadmap generated yet.
            </div>
          ) : (
            <div className="grid gap-5 md:grid-cols-2">
              {result.roadmap.map((item) => (
                <div
                  key={item.skill}
                  className="rounded-3xl border border-gray-200 bg-white p-5"
                >
                  <div className="mb-3 flex items-center justify-between">
                    <div className="text-lg font-black text-gray-950">
                      Priority {item.priority}: {item.skill}
                    </div>
                    <Badge variant="purple">Roadmap</Badge>
                  </div>

                  <ul className="space-y-2 text-sm leading-6 text-gray-600">
                    {item.learning_steps.map((step) => (
                      <li key={step}>• {step}</li>
                    ))}
                  </ul>

                  <div className="mt-4 rounded-2xl bg-green-50 p-4">
                    <div className="text-sm font-black text-green-700">
                      Portfolio Task
                    </div>
                    <p className="mt-1 text-sm text-green-800">
                      {item.portfolio_task}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </SectionCard>
      </section>
    </main>
  );
}