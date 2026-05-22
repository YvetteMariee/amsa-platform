import { useState } from "react"
import api from "../services/api"

interface Props {
  onLogin: (token: string) => void
}

export default function Login({ onLogin }: Props) {
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    try {
      const formData = new URLSearchParams()
      formData.append("username", username)
      formData.append("password", password)

      const response = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" }
      })
      onLogin(response.data.access_token)
    } catch (err) {
      setError("Échec de connexion. Vérifiez vos identifiants.")
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950 text-slate-100 p-4">
      <div className="w-full max-w-md rounded-[2rem] border border-slate-800 bg-slate-900/95 p-8 shadow-2xl shadow-slate-900/40">
        <h1 className="mb-6 text-3xl font-bold text-cyan-400">Connexion AMSA</h1>
        <form className="space-y-5" onSubmit={handleSubmit}>
          <div>
            <label className="mb-2 block text-sm text-slate-300">Utilisateur</label>
            <input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-cyan-500"
              placeholder="admin"
            />
          </div>
          <div>
            <label className="mb-2 block text-sm text-slate-300">Mot de passe</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-cyan-500"
              placeholder="••••••••"
            />
          </div>
          {error && <div className="text-sm text-rose-400">{error}</div>}
          <button className="w-full rounded-2xl bg-cyan-500 px-4 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400">Se connecter</button>
        </form>
      </div>
    </div>
  )
}
