import Link from "next/link";
import { BrainCircuit, BriefcaseBusiness, ChartNoAxesCombined, Compass, Home, PoundSterling } from "lucide-react";

const navItems = [
  {
    href: "/",
    label: "Home",
    icon: Home,
  },
  {
    href: "/market",
    label: "Market",
    icon: ChartNoAxesCombined,
  },
  {
    href: "/cv-match",
    label: "CV Match",
    icon: BriefcaseBusiness,
  },
  {
    href: "/salary",
    label: "Salary",
    icon: PoundSterling,
  },
  {
    href: "/skill-gap",
    label: "Skill Gap",
    icon: Compass,
  },
];

export function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white/85 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-700 to-green-500 text-white shadow-lg">
            <BrainCircuit size={24} />
          </div>
          <div>
            <div className="text-lg font-black tracking-tight text-gray-950">
              SkillLens AI
            </div>
            <div className="text-xs font-semibold text-gray-500">
              Workforce Intelligence Platform
            </div>
          </div>
        </Link>

        <nav className="hidden items-center gap-2 md:flex">
          {navItems.map((item) => {
            const Icon = item.icon;

            return (
              <Link
                key={item.href}
                href={item.href}
                className="flex items-center gap-2 rounded-2xl px-4 py-2 text-sm font-bold text-gray-700 transition hover:bg-purple-50 hover:text-purple-700"
              >
                <Icon size={16} />
                {item.label}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}