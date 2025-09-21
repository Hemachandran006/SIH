import { useEffect, useState } from 'react'
import { api } from '../api/client'
import { FileDown } from 'lucide-react'
import { motion } from 'framer-motion'

type Log = {
  id: number
  device_uid: string
  method: string
  status: string
  started_at: string
  completed_at?: string
}

export default function Logs() {
  const [logs, setLogs] = useState<Log[]>([])
  const [loading, setLoading] = useState(true)
  const [downloadingId, setDownloadingId] = useState<number | null>(null)

  useEffect(() => {
    (async () => {
      try {
        const items = await api.getWipes()
        setLogs(items)
      } finally {
        setLoading(false)
      }
    })()
  }, [])

  const download = async (id: number) => {
    try {
      setDownloadingId(id)
      const { blob, filename } = await api.downloadCertificate(id)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    } finally {
      setDownloadingId(null)
    }
  }

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="card">
      <h3 className="font-semibold mb-3">Wipe Logs</h3>
      {loading ? (
        <div className="text-sm text-slate-500">Loading...</div>
      ) : (
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Device UID</th>
                <th>Method</th>
                <th>Status</th>
                <th>Started</th>
                <th>Completed</th>
                <th>Certificate</th>
              </tr>
            </thead>
            <tbody>
              {logs.map(l => {
                const canDownload = l.status === 'verified' || l.status === 'wiped'
                return (
                  <tr key={l.id}>
                    <td>{l.id}</td>
                    <td className="font-mono">{l.device_uid}</td>
                    <td>{l.method}</td>
                    <td>
                      <span className={`px-2 py-1 rounded-lg text-xs ${
                        l.status === 'verified' ? 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-300' :
                        l.status === 'wiped' ? 'bg-blue-500/15 text-blue-600 dark:text-blue-300' :
                        l.status === 'in_progress' ? 'bg-amber-500/15 text-amber-600 dark:text-amber-300' :
                        'bg-slate-500/15 text-slate-600 dark:text-slate-300'
                      }`}>{l.status}</span>
                    </td>
                    <td>{new Date(l.started_at).toLocaleString()}</td>
                    <td>{l.completed_at ? new Date(l.completed_at).toLocaleString() : '-'}</td>
                    <td>
                      <button
                        className="btn btn-ghost"
                        onClick={() => download(l.id)}
                        disabled={!canDownload || downloadingId === l.id}
                        title={!canDownload ? 'Available after wipe completion' : 'Download PDF'}
                      >
                        <FileDown size={16} />
                        {downloadingId === l.id ? 'Preparing…' : 'PDF'}
                      </button>
                    </td>
                  </tr>
                )
              })}
              {logs.length === 0 && (
                <tr><td colSpan={7} className="text-center text-sm text-slate-500 py-6">No logs yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </motion.div>
  )
}