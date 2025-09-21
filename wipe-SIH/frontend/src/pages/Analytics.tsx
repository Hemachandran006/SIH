import { useEffect, useMemo, useState } from 'react'
import { api } from '../api/client'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { motion } from 'framer-motion'

type Log = { method: string }

const COLORS = ['#6366f1', '#22c55e', '#f43f5e', '#06b6d4', '#f59e0b']

export default function Analytics() {
  const [logs, setLogs] = useState<Log[]>([])
  useEffect(() => {
    (async () => {
      const items = await api.getWipes()
      setLogs(items)
    })()
  }, [])

  const data = useMemo(() => {
    const counts: Record<string, number> = {}
    logs.forEach(l => { counts[l.method] = (counts[l.method] || 0) + 1 })
    return Object.entries(counts).map(([name, value]) => ({ name, value }))
  }, [logs])

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="card">
      <h3 className="font-semibold mb-3">Wipe Methods Usage</h3>
      <div className="h-[360px]">
        {data.length === 0 ? (
          <div className="text-sm text-slate-500">No data yet.</div>
        ) : (
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie dataKey="value" data={data} cx="50%" cy="50%" outerRadius={120} label>
                {data.map((entry, index) => (<Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>
    </motion.div>
  )
}