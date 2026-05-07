"use client";

import { useState } from "react";
import { predictSalary } from "@/lib/api";
import { SalaryPredictionResponse } from "@/lib/types";
import { formatCurrency } from "@/lib/utils";
import { SectionCard } from "@/components/SectionCard";

const categories = [
  "Data Analyst",
  "Data Scientist",
  "Data Engineer",
  "Machine Learning Engineer",
  "BI Analyst",
  "Analytics Engineer",
  "AI Engineer",
];

const levels = ["Entry Level", "Junior", "Mid Level", "Senior"];
const workTypes = ["Remote", "Hybrid", "Onsite"];
const locations = [
  "London",
  "Newcastle",
  "Manchester",
  "Edinburgh",
  "Glasgow",
  "Birmingham",
  "Leeds",
  "Bristol",
  "Remote UK",
];

export default function SalaryPage() {
  const [category, setCategory] = useState("Data Scientist");
  const [experienceLevel, setExperienceLevel] = useState("Mid Level");
  const [workType, setWorkType] = useState("Hybrid");
  const [location, setLocation] = useState("London");
  const [skillCount, setSkillCount] = useState(8);
  const [result, setResult] = useState<SalaryPredictionResponse | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handlePredict() {
    setLoading(true);
    setError("");

    try {
      const data = await predictSalary({
        category,
        experience_level: experienceLevel,
        work_type: workType,
        location,
        skill_count: skillCount,
      });

      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Prediction failed.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <div className="mb-10">
        <h1 className="text-4xl font-black tracking-tight text-gray-950">
          Salary Predictor
        </h1>
        <p className="mt-3 max-w-2xl text-gray-600">
          Estimate salary ranges using the Stage 2 machine learning regression
          model served through FastAPI.
        </p>
      </div>

      <section className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Prediction Inputs">
          <div className="grid gap-4">
            <label className="text-sm font-black text-gray-700">Role Category</label>
            <select className="input-style" value={category} onChange={(e) => setCategory(e.target.value)}>
              {categories.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>

            <label className="text-sm font-black text-gray-700">Experience Level</label>
            <select className="input-style" value={experienceLevel} onChange={(e) => setExperienceLevel(e.target.value)}>
              {levels.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>

            <label className="text-sm font-black text-gray-700">Work Type</label>
            <select className="input-style" value={workType} onChange={(e) => setWorkType(e.target.value)}>
              {workTypes.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>

            <label className="text-sm font-black text-gray-700">Location</label>
            <select className="input-style" value={location} onChange={(e) => setLocation(e.target.value)}>
              {locations.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>

            <label className="text-sm font-black text-gray-700">
              Relevant Skill Count: {skillCount}
            </label>
            <input
              type="range"
              min={1}
              max={20}
              value={skillCount}
              onChange={(event) => setSkillCount(Number(event.target.value))}
            />

            <button className="btn-primary mt-3" onClick={handlePredict}>
              {loading ? "Predicting..." : "Predict Salary"}
            </button>

            {error ? (
              <div className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm font-semibold text-red-700">
                {error}
              </div>
            ) : null}
          </div>
        </SectionCard>

        <SectionCard title="Predicted Salary Range">
          {result ? (
            <div>
              <div className="text-6xl font-black tracking-tight text-purple-700">
                {formatCurrency(result.estimated_lower_range)} -{" "}
                {formatCurrency(result.estimated_upper_range)}
              </div>
              <div className="mt-4 rounded-2xl bg-green-50 p-5">
                <div className="text-sm font-black uppercase tracking-wide text-green-700">
                  Predicted Midpoint
                </div>
                <div className="mt-1 text-3xl font-black text-green-700">
                  {formatCurrency(result.predicted_salary_midpoint)}
                </div>
              </div>
              <p className="mt-5 text-sm leading-6 text-gray-500">
                This prediction is generated by the Stage 2 Random Forest
                salary model trained on the SkillLens sample job dataset.
              </p>
            </div>
          ) : (
            <div className="rounded-2xl bg-gray-50 p-5 text-gray-500">
              Choose inputs and run the prediction.
            </div>
          )}
        </SectionCard>
      </section>
    </main>
  );
}