"use client";

import { useEffect, useState } from "react";
import { BarChart, Bar, CartesianGrid, Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { Building2, BriefcaseBusiness, MapPin, PoundSterling, Sparkles } from "lucide-react";
import { getCategories, getJobs, getJobSummary, getSalaryByCategory, getTopSkills } from "@/lib/api";
import { CategoryCount, JobPosting, JobSummary, SalaryByCategory, SkillCount } from "@/lib/types";
import { formatCurrency, formatNumber } from "@/lib/utils";
import { StatCard } from "@/components/StatCard";
import { SectionCard } from "@/components/SectionCard";
import { JobTable } from "@/components/JobTable";

const COLORS = ["#6D28D9", "#22C55E", "#A78BFA", "#86EFAC", "#4C1D95", "#15803D"];

export default function MarketPage() {
  const [summary, setSummary] = useState<JobSummary | null>(null);
  const [categories, setCategories] = useState<CategoryCount[]>([]);
  const [skills, setSkills] = useState<SkillCount[]>([]);
  const [salary, setSalary] = useState<SalaryByCategory[]>([]);
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const [summaryData, categoryData, skillData, salaryData, jobData] =
          await Promise.all([
            getJobSummary(),
            getCategories(),
            getTopSkills(15),
            getSalaryByCategory(),
            getJobs(20),
          ]);

        setSummary(summaryData);
        setCategories(categoryData);
        setSkills(skillData);
        setSalary(salaryData);
        setJobs(jobData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load data.");
      }
    }

    load();
  }, []);

  if (error) {
    return (
      <main className="mx-auto max-w-7xl px-6 py-12">
        <div className="rounded-3xl border border-red-200 bg-red-50 p-6 text-red-700">
          <h1 className="text-xl font-black">Backend connection error</h1>
          <p className="mt-2 text-sm">{error}</p>
          <p className="mt-4 text-sm">
            Make sure FastAPI is running with:{" "}
            <code>uvicorn backend.main:app --reload</code>
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="mx-auto max-w-7xl px-6 py-12">
      <div className="mb-10">
        <h1 className="text-4xl font-black tracking-tight text-gray-950">
          Market Intelligence
        </h1>
        <p className="mt-3 max-w-2xl text-gray-600">
          Explore job demand, skill trends and salary intelligence from the
          SkillLens AI data platform.
        </p>
      </div>

      <section className="grid gap-5 md:grid-cols-2 lg:grid-cols-5">
        <StatCard
          label="Jobs"
          value={formatNumber(summary?.total_jobs)}
          icon={<BriefcaseBusiness size={20} />}
        />
        <StatCard
          label="Companies"
          value={formatNumber(summary?.companies)}
          icon={<Building2 size={20} />}
        />
        <StatCard
          label="Locations"
          value={formatNumber(summary?.locations)}
          icon={<MapPin size={20} />}
        />
        <StatCard
          label="Avg Salary"
          value={formatCurrency(summary?.avg_salary)}
          icon={<PoundSterling size={20} />}
        />
        <StatCard
          label="Skills"
          value={formatNumber(summary?.skills)}
          icon={<Sparkles size={20} />}
        />
      </section>

      <section className="mt-8 grid gap-6 lg:grid-cols-2">
        <SectionCard title="Job Demand by Category">
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={categories}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="category" tick={{ fontSize: 11 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" radius={[12, 12, 0, 0]}>
                  {categories.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>

        <SectionCard title="Average Salary by Category">
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={salary}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="category" tick={{ fontSize: 11 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="avg_salary" radius={[12, 12, 0, 0]}>
                  {salary.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>
      </section>

      <section className="mt-8 grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <SectionCard title="Top Skills">
          <div className="space-y-3">
            {skills.map((skill, index) => (
              <div
                key={skill.skill}
                className="flex items-center justify-between rounded-2xl border border-gray-200 bg-gray-50 px-4 py-3"
              >
                <div className="font-black text-gray-800">
                  {index + 1}. {skill.skill}
                </div>
                <div className="rounded-full bg-purple-100 px-3 py-1 text-sm font-black text-purple-700">
                  {skill.count}
                </div>
              </div>
            ))}
          </div>
        </SectionCard>

        <SectionCard title="Category Mix">
          <div className="h-96">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={categories}
                  dataKey="count"
                  nameKey="category"
                  outerRadius={140}
                  label
                >
                  {categories.map((_, index) => (
                    <Cell key={index} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </SectionCard>
      </section>

      <section className="mt-8">
        <SectionCard title="Job Explorer">
          <JobTable jobs={jobs} />
        </SectionCard>
      </section>
    </main>
  );
}