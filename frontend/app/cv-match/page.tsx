"use client";

import { useState } from "react";
import { matchCvToJobs } from "@/lib/api";
import { CVMatchResult } from "@/lib/types";
import { SectionCard } from "@/components/SectionCard";
import { Badge } from "@/components/Badge";

const exampleCv = `Data Scientist with experience in Python, SQL, Pandas, NumPy, scikit-learn, machine learning, Power BI, Tableau, FastAPI, Docker, PostgreSQL and forecasting. Built dashboards, predictive models and data pipelines for business insight.`;

export default function CvMatchPage() {
  const [cvText, setCvText] = useState(exampleCv);
  const [results, setResults] = useState<CVMatchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAnalyse() {
    setLoading(true);
    setError("");

    try {
      const data = await matchCvToJobs(cvText, 15);
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to analyse CV.");
    } finally {
      setLoading(false);
    }
  }

  const best = results[0];

  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <div className="mb-10">
        <h1 className="text-4xl font-black tracking-tight text-gray-950">
          CV Job Matcher
        </h1>
        <p className="mt-3 max-w-2xl text-gray-600">
          Paste CV text and rank job postings by skill match score using the
          SkillLens AI matching engine.
        </p>
      </div>

      <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <SectionCard
          title="Paste CV Text"
          description="The backend extracts technical skills and compares them against job requirements."
        >
          <textarea
            className="input-style min-h-72"
            value={cvText}
            onChange={(event) => setCvText(event.target.value)}
          />

          <button
            className="btn-primary mt-5"
            onClick={handleAnalyse}
            disabled={loading}
          >
            {loading ? "Analysing..." : "Analyse CV Match"}
          </button>

          {error ? (
            <div className="mt-5 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm font-semibold text-red-700">
              {error}
            </div>
          ) : null}
        </SectionCard>

        <SectionCard title="Best Match Summary">
          {best ? (
            <div>
              <div className="text-6xl font-black text-purple-700">
                {best.match_score}%
              </div>
              <div className="mt-2 text-lg font-black text-gray-950">
                {best.title}
              </div>
              <div className="mt-1 text-gray-500">
                {best.company} • {best.location}
              </div>

              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                <div className="rounded-2xl bg-green-50 p-4">
                  <div className="text-sm font-bold text-green-700">
                    Matched Skills
                  </div>
                  <div className="mt-1 text-2xl font-black text-green-700">
                    {best.matched_skill_count}
                  </div>
                </div>
                <div className="rounded-2xl bg-purple-50 p-4">
                  <div className="text-sm font-bold text-purple-700">
                    Required Skills
                  </div>
                  <div className="mt-1 text-2xl font-black text-purple-700">
                    {best.required_skill_count}
                  </div>
                </div>
              </div>

              <div className="mt-5">
                <div className="mb-2 text-sm font-black text-gray-600">
                  Matched
                </div>
                <div className="flex flex-wrap gap-2">
                  {best.matched_skills.map((skill) => (
                    <Badge key={skill} variant="green">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>

              <div className="mt-5">
                <div className="mb-2 text-sm font-black text-gray-600">
                  Missing
                </div>
                <div className="flex flex-wrap gap-2">
                  {best.missing_skills.map((skill) => (
                    <Badge key={skill} variant="purple">
                      {skill}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="rounded-2xl bg-gray-50 p-5 text-gray-500">
              Run the analysis to see your best job match.
            </div>
          )}
        </SectionCard>
      </section>

      <section className="mt-8">
        <SectionCard title="Ranked Job Matches">
          {results.length === 0 ? (
            <div className="rounded-2xl bg-gray-50 p-5 text-gray-500">
              No results yet.
            </div>
          ) : (
            <div className="space-y-4">
              {results.map((job) => (
                <div
                  key={job.job_id || `${job.title}-${job.company}`}
                  className="rounded-3xl border border-gray-200 bg-white p-5"
                >
                  <div className="flex flex-wrap items-start justify-between gap-4">
                    <div>
                      <div className="text-lg font-black text-gray-950">
                        {job.title}
                      </div>
                      <div className="mt-1 text-sm text-gray-500">
                        {job.company} • {job.location} • {job.category}
                      </div>
                    </div>
                    <div className="rounded-full bg-gradient-to-r from-purple-700 to-green-500 px-4 py-2 text-sm font-black text-white">
                      {job.match_score}% Match
                    </div>
                  </div>

                  <div className="mt-4 grid gap-4 md:grid-cols-2">
                    <div>
                      <div className="mb-2 text-sm font-black text-green-700">
                        Matched Skills
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {job.matched_skills.map((skill) => (
                          <Badge key={skill} variant="green">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>

                    <div>
                      <div className="mb-2 text-sm font-black text-purple-700">
                        Missing Skills
                      </div>
                      <div className="flex flex-wrap gap-2">
                        {job.missing_skills.map((skill) => (
                          <Badge key={skill} variant="purple">
                            {skill}
                          </Badge>
                        ))}
                      </div>
                    </div>
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