import { Link, useLocation } from 'react-router-dom'
import { ThemeToggle } from './ThemeToggle'
import { ShieldCheck, LogOut, LayoutDashboard, HardDrive, List, BarChart2 } from 'lucide-react'
import { useAuth } from '../context/AuthContext'

const NavLink = ({ to, label, icon: Icon }: { to: string; label: string; icon: any }) => {
  const { pathname } = useLocation()
  const active = pathname === to
  return (
    <Link
      to={to}
      className={`px-3 py-2 rounded-xl text-sm font-medium flex items-center gap-2 hover:bg-black/5 dark:hover:bg-white/10 transition-colors ${
        active ? 'bg-black/10 dark:bg-white/10' : ''
      }`}
    >
      <Icon size={18} />
      {label}
    </Link>
  )
}

export function Navbar() {
  const { logout } = useAuth()
  return (
    <header className="sticky top-0 z-30 backdrop-blur-xl bg-white/60 dark:bg-black/20 border-b border-black/10 dark:border-white/10">
      <div className="max-w-7xl mx-auto px-4 md:px-6 py-3 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-2xl bg-gradient-to-tr from-blue-500 to-indigo-600 flex items-center justify-center text-white shadow-soft">
            <ShieldCheck size={18} />
          </div>
          <span className="font-semibold text-lg tracking-tight">EraseX</span>
        </div>
        <nav className="hidden md:flex items-center gap-1">
          <NavLink to="/" label="Dashboard" icon={LayoutDashboard} />
          <NavLink to="/simulator" label="Device Simulator" icon={HardDrive} />
          <NavLink to="/logs" label="Logs" icon={List} />
          <NavLink to="/analytics" label="Analytics" icon={BarChart2} />
        </nav>
        <div className="flex items-center gap-2">
          <ThemeToggle />
          <button className="btn btn-ghost" onClick={logout} title="Logout">
            <LogOut size={18} />
          </button>
        </div>
      </div>
    </header>
  )
}