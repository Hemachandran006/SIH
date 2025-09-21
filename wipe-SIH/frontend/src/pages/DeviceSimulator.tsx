import { motion } from 'framer-motion'
import { useState } from 'react'
import { api } from '../api/client'
import { HardDrive, Rocket, Scan, ShieldCheck, FileDown } from 'lucide-react'

const methods = ["NIST", "DoD 5220.22-M", "Gutmann", "Quick Zero Fill"]

export default function DeviceSimulator() {
  const [device, setDevice] = useState<{ id: number; device_uid: string; name: string; type: string } | null>(null)
  const [selectedMethod, setSelectedMethod] = useState<string>(methods[0])
  const [wipe, setWipe] = useState<{ id: number; status: string } | null>(null)
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)
  const [downloading, setDownloading] = useState(false)

  const scan = async () => {
    setLoading(true)
    try {
      const d = await api.scanDevice()
      setDevice(d)
      setWipe(null)
      setProgress(0)
    } finally {
      setLoading(false)
    }
  }

  const startWipe = async () => {
    if (!device) return
    setLoading(true)
    setProgress(10)
    try {
      const wl = await api.startWipe(device.device_uid, selectedMethod)
      setWipe({ id: wl.id, status: wl.status })
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 95) {
            clearInterval(interval)
            return 95
          }
          return prev + Math.random() * 10
        })
      }, 300)
      setTimeout(() => {
        setProgress(100)
        setWipe(w => w ? { ...w, status: 'wiped' } : w)
      }, 2500)
    } finally {
      setLoading(false)
    }
  }

  const verify = async () => {
    if (!wipe) return
    const res = await api.verifyWipe(wipe.id)
    setWipe({ id: res.id, status: res.status })
  }

  const downloadCertificate = async () => {
    if (!wipe) return
    try {
      setDownloading(true)
      const { blob, filename } = await api.downloadCertificate(wipe.id)
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)
    } finally {
      setDownloading(false)
    }
  }

  const canDownload = wipe?.status === 'verified' || wipe?.status === 'wiped'

  return (
    <div className="grid lg:grid-cols-3 gap-6">
      <motion.div className="card lg:col-span-2" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex items-center gap-3 mb-4">
          <div className="h-10 w-10 rounded-2xl bg-gradient-to-tr from-blue-500 to-indigo-600 text-white flex items-center justify-center shadow-soft">
            <HardDrive size={20} />
          </div>
          <div>
            <h3 className="font-semibold">Device Simulator</h3>
            <p className="text-sm text-slate-500 dark:text-slate-400">Scan, wipe, verify, and certify.</p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          <div className="p-4 rounded-2xl bg-white/50 dark:bg-white/5 border border-black/10 dark:border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <div className="h-9 w-9 rounded-xl bg-black/10 dark:bg-white/10 flex items-center justify-center">
                <Scan size={18} />
              </div>
              <div className="font-medium">Scan Device</div>
            </div>
            {device ? (
              <div className="text-sm space-y-1">
                <div><span className="text-slate-500">UID:</span> {device.device_uid}</div>
                <div><span className="text-slate-500">Name:</span> {device.name}</div>
                <div><span className="text-slate-500">Type:</span> {device.type}</div>
              </div>
            ) : (
              <p className="text-sm text-slate-500">No device detected.</p>
            )}
            <button className="btn btn-primary mt-4" onClick={scan} disabled={loading}>
              {loading ? 'Scanning...' : 'Scan'}
            </button>
          </div>

          <div className="p-4 rounded-2xl bg-white/50 dark:bg-white/5 border border-black/10 dark:border-white/10">
            <div className="flex items-center gap-3 mb-3">
              <div className="h-9 w-9 rounded-xl bg-black/10 dark:bg-white/10 flex items-center justify-center">
                <Rocket size={18} />
              </div>
              <div className="font-medium">Wipe Method</div>
            </div>
            <select className="input" value={selectedMethod} onChange={e => setSelectedMethod(e.target.value)} disabled={!device || !!wipe}>
              {methods.map(m => <option key={m} value={m}>{m}</option>)}
            </select>
            <button className="btn btn-primary mt-4" onClick={startWipe} disabled={!device || loading || !!wipe}>
              Start Wipe
            </button>
            {wipe && (
              <div className="mt-4">
                <div className="text-sm mb-2">Status: <span className="font-medium">{wipe.status}</span></div>
                <div className="w-full bg-black/10 dark:bg-white/10 rounded-full h-2 overflow-hidden">
                  <div className="h-2 rounded-full bg-gradient-to-r from-blue-500 to-indigo-600 transition-all" style={{ width: `${progress}%` }} />
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="mt-6 p-4 rounded-2xl bg-white/50 dark:bg-white/5 border border-black/10 dark:border-white/10">
          <div className="flex items-center gap-3 mb-3">
            <div className="h-9 w-9 rounded-xl bg-black/10 dark:bg-white/10 flex items-center justify-center">
              <ShieldCheck size={18} />
            </div>
            <div className="font-medium">Verification & Certificate</div>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            <button className="btn btn-primary" onClick={verify} disabled={!wipe || wipe.status === 'verified'}>
              Verify Wipe
            </button>
            <button
              className="btn btn-ghost"
              onClick={downloadCertificate}
              disabled={!canDownload || downloading}
              title={!canDownload ? 'Complete wipe or verification first' : 'Download PDF certificate'}
            >
              <FileDown size={18} />
              {downloading ? 'Preparing…' : 'Download Certificate'}
            </button>
          </div>
          <p className="text-xs text-slate-500 mt-2">Verification uses an AI check in this prototype and returns success.</p>
        </div>
      </motion.div>

      <motion.aside className="card" initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
        <h3 className="font-semibold mb-3">Guided Steps</h3>
        <ol className="list-decimal ml-4 text-sm space-y-2 text-slate-600 dark:text-slate-400">
          <li>Click Scan to detect a simulated device.</li>
          <li>Select an industry-standard wipe method.</li>
          <li>Start Wipe and watch real-time progress.</li>
          <li>Verify Wipe to finalize the process.</li>
          <li>Download the signed certificate.</li>
        </ol>
      </motion.aside>
    </div>
  )
}