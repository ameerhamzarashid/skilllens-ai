import { JobPosting } from "@/lib/types";
import { formatCurrency, truncate } from "@/lib/utils";
import { Badge } from "@/components/Badge";

type JobTableProps = {
  jobs: JobPosting[];
};

export function JobTable({ jobs }: JobTableProps) {
  return (
    <div className="table-wrapper rounded-3xl border border-gray-200 bg-white">
      <table>
        <thead>
          <tr>
            <th>Role</th>
            <th>Company</th>
            <th>Location</th>
            <th>Work Type</th>
            <th>Salary</th>
            <th>Skills</th>
          </tr>
        </thead>
        <tbody>
          {jobs.map((job, index) => (
            <tr key={`${job.job_id}-${index}`}>
              <td>
                <div className="font-black text-gray-950">{job.title}</div>
                <div className="mt-1 text-xs text-gray-500">{job.category}</div>
              </td>
              <td>{job.company}</td>
              <td>{job.location}</td>
              <td>
                <Badge variant="green">{job.work_type || "N/A"}</Badge>
              </td>
              <td>
                {formatCurrency(job.salary_min)} - {formatCurrency(job.salary_max)}
              </td>
              <td className="max-w-sm text-sm text-gray-600">
                {truncate(job.extracted_skills, 120)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}