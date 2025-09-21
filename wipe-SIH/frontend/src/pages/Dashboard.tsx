import { motion } from 'framer-motion'
import { HardDrive, FileCheck2, ChartPie } from 'lucide-react'
import { Link } from 'react-router-dom'

const Card = ({ to, icon: Icon, title, desc, gradient }: { to: string; icon: any; title: string; desc: string; gradient: string }) => (
  <motion.div whileHover={{ y: -4 }} transition={{ type: 'spring', stiffness: 250, damping: 20 }}>
    <Link to={to} className="card block">
      <div className={`h-12 w-12 rounded-2xl ${gradient} text-white flex items-center justify-center shadow-soft mb-4`}>
        <Icon size={22} />
      </div>
      <h3 className="font-semibold text-lg">{title}</h3>
      <p className="text-sm text-slate-600 dark:text-slate-400 mt-1">{desc}</p>
    </Link>
  </motion.div>
)

export default function Dashboard() {
  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl font-semibold tracking-tight">Dashboard</h2>
        <p className="text-slate-600 dark:text-slate-400">Smooth, modern control center for secure device sanitization.</p>
      </div>

      <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card
          to="/simulator"
          icon={HardDrive}
          title="Device Simulator"
          desc="Scan devices, choose wipe methods, run wipes, and verify."
          gradient="bg-gradient-to-tr from-blue-500 to-indigo-600"
        />
        <Card
          to="/logs"
          icon={FileCheck2}
          title="Logs & Reports"
          desc="Browse your wipe history and download certificates."
          gradient="bg-gradient-to-tr from-emerald-500 to-teal-600"
        />
        <Card
          to="/analytics"
          icon={ChartPie}
          title="Analytics"
          desc="Visualize wipe methods usage at a glance."
          gradient="bg-gradient-to-tr from-fuchsia-500 to-pink-600"
        />
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="card lg:col-span-2">
          <h3 className="font-semibold mb-2">Welcome</h3>
          <p className="text-slate-600 dark:text-slate-400">
            Start by scanning a device in the simulator. You can perform a secure wipe using industry-standard methods
            and generate a formal certificate upon completion.
          </p>
        </div>
        <div className="card">
          <h3 className="font-semibold mb-2">Quick Start</h3>
          <ol className="text-sm list-decimal ml-4 space-y-1 text-slate-600 dark:text-slate-400">
            <li>Go to Device Simulator</li>
            <li>Scan device and choose wipe method</li>
            <li>Start wipe, then Verify</li>
            <li>Download certificate</li>
          </ol>
        </div>
      </div>
    </div>
  )
}