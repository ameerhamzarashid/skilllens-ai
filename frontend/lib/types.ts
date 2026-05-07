export type JobSummary = {
  total_jobs: number;
  companies: number;
  locations: number;
  avg_salary: number;
  skills: number;
};

export type SkillCount = {
  skill: string;
  count: number;
};

export type CategoryCount = {
  category: string;
  count: number;
};

export type SalaryByCategory = {
  category: string;
  avg_salary: number;
};

export type JobPosting = {
  job_id?: string | null;
  title?: string | null;
  company?: string | null;
  location?: string | null;
  country?: string | null;
  category?: string | null;
  experience_level?: string | null;
  work_type?: string | null;
  salary_min?: number | null;
  salary_max?: number | null;
  salary_currency?: string | null;
  extracted_skills?: string | null;
  posted_date?: string | null;
  source?: string | null;
};

export type CVMatchResult = {
  job_id?: string | null;
  title?: string | null;
  company?: string | null;
  location?: string | null;
  category?: string | null;
  match_score: number;
  matched_skills: string[];
  missing_skills: string[];
  extra_cv_skills: string[];
  required_skill_count: number;
  matched_skill_count: number;
};

export type MissingSkill = {
  skill: string;
  missing_count: number;
};

export type RoadmapItem = {
  priority: number;
  skill: string;
  learning_steps: string[];
  portfolio_task: string;
};

export type SkillGapResponse = {
  missing_skills: MissingSkill[];
  roadmap: RoadmapItem[];
};

export type SalaryPredictionResponse = {
  predicted_salary_midpoint: number;
  estimated_lower_range: number;
  estimated_upper_range: number;
};