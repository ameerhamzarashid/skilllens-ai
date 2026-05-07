import {
  CategoryCount,
  CVMatchResult,
  JobPosting,
  JobSummary,
  SalaryByCategory,
  SalaryPredictionResponse,
  SkillCount,
  SkillGapResponse,
} from "@/lib/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";

async function apiFetch<T>(
  path: string,
  options?: RequestInit,
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options?.headers || {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export async function getJobSummary(): Promise<JobSummary> {
  return apiFetch<JobSummary>("/jobs/summary");
}

export async function getJobs(limit = 20): Promise<JobPosting[]> {
  return apiFetch<JobPosting[]>(`/jobs?limit=${limit}`);
}

export async function getTopSkills(limit = 20): Promise<SkillCount[]> {
  return apiFetch<SkillCount[]>(`/skills/top?limit=${limit}`);
}

export async function getCategories(): Promise<CategoryCount[]> {
  return apiFetch<CategoryCount[]>("/jobs/categories");
}

export async function getSalaryByCategory(): Promise<SalaryByCategory[]> {
  return apiFetch<SalaryByCategory[]>("/jobs/salary-by-category");
}

export async function matchCvToJobs(
  cvText: string,
  topN = 10,
): Promise<CVMatchResult[]> {
  return apiFetch<CVMatchResult[]>("/cv/match-jobs", {
    method: "POST",
    body: JSON.stringify({
      cv_text: cvText,
      top_n: topN,
    }),
  });
}

export async function analyseSkillGap(
  cvText: string,
  topN = 10,
): Promise<SkillGapResponse> {
  return apiFetch<SkillGapResponse>("/cv/skill-gap", {
    method: "POST",
    body: JSON.stringify({
      cv_text: cvText,
      top_n: topN,
    }),
  });
}

export async function predictSalary(payload: {
  category: string;
  experience_level: string;
  work_type: string;
  location: string;
  skill_count: number;
}): Promise<SalaryPredictionResponse> {
  return apiFetch<SalaryPredictionResponse>("/ml/predict-salary", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}