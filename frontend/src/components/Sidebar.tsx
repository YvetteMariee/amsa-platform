import { NavLink } from "react-router-dom"

interface Props {
  onLogout: () => void
}

const links = [
  { href: "/", label: "Dashboard" },
  { href: "/upload", label: "Upload" },
  { href: "/alerts", label: "Alerts" },
  { href: "/reports", label: "Reports" }
]

export default function Sidebar({ onLogout }: Props) {
  return (
    <aside className="w-full md:w-72 border-r border-slate-800 bg-slate-950/90 p-6">
      <div className="mb-10">
        <p className="text-3xl font-semibold text-cyan-400">AMSA</p>
        <p className="text-slate-400 mt-2">Surveillance marché CEMAC</p>
      </div>
      <nav className="space-y-2">
        {links.map((link) => (
          <NavLink
            key={link.href}
            to={link.href}
            className={({ isActive }) =>
              `block rounded-2xl px-4 py-3 text-slate-100 transition ${isActive ? "bg-slate-800" : "hover:bg-slate-800/70"}`
            }
          >
            {link.label}
          </NavLink>
        ))}
      </nav>
      <button
        onClick={onLogout}
        className="mt-10 w-full rounded-2xl bg-cyan-500 px-4 py-3 text-slate-950 font-semibold shadow-lg shadow-cyan-500/20 transition hover:bg-cyan-400"
      >
        Déconnexion
      </button>
    </aside>
  )
}
