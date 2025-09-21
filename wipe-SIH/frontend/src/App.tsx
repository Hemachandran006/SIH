import { Routes, Route, Navigate } from 'react-router-dom'
import { Navbar } from './components/Navbar'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import DeviceSimulator from './pages/DeviceSimulator'
import Logs from './pages/Logs'
import Analytics from './pages/Analytics'
import { useAuth } from './context/AuthContext'
import { motion } from 'framer-motion'

function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { isAuthenticated } = useAuth()
  if (!isAuthenticated) return <Navigate to="/login" replace />
  return children
}

export default function App() {
  return (
    <div className="min-h-screen text-slate-900 dark:text-slate-100">
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route
          path="/*"
          element={
            <ProtectedRoute>
              <div>
                <Navbar />
                <motion.main
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.4 }}
                  className="max-w-7xl mx-auto px-4 md:px-6 py-8"
                >
                  <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/simulator" element={<DeviceSimulator />} />
                    <Route path="/logs" element={<Logs />} />
                    <Route path="/analytics" element={<Analytics />} />
                  </Routes>
                </motion.main>
              </div>
            </ProtectedRoute>
          }
        />
      </Routes>
    </div>
  )
}