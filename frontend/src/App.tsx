import { Route, Routes, Navigate } from "react-router-dom"
import { useState } from "react"
import Dashboard from "./pages/Dashboard"
import Upload from "./pages/Upload"
import Alerts from "./pages/Alerts"
import Reports from "./pages/Reports"
import Login from "./pages/Login"
import Sidebar from "./components/Sidebar"

function App() {
  const [token, setToken] = useState(localStorage.getItem("amsa_token") || "")

  const handleLogin = (newToken: string) => {
    localStorage.setItem("amsa_token", newToken)
    setToken(newToken)
  }

  const handleLogout = () => {
    localStorage.removeItem("amsa_token")
    setToken("")
  }

  if (!token) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="flex flex-col md:flex-row">
        <Sidebar onLogout={handleLogout} />
        <main className="flex-1 p-6">
          <div className="mb-6 rounded-3xl bg-slate-900/80 p-6 shadow-2xl shadow-slate-900/20">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/upload" element={<Upload />} />
              <Route path="/alerts" element={<Alerts />} />
              <Route path="/reports" element={<Reports />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
