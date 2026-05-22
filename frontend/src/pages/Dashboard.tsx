import { useEffect, useState } from "react"
import api from "../services/api"
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts"

export default function Dashboard() {
  const [metrics, setMetrics] = useState<any>(null)
  const [errors, setErrors] = useState("")

  useEffect(() => {
    api.get("/analytics/market_data")
      .then((response) => setMetrics(response.data))
      .catch((err) => setErrors("Impossible de charger les données du marché."))
  }, [])

  const chartData = metrics
    ? [
        { name: "Prix moyen", value: metrics.average_price || 0 },
        { name: "Volume total", value: metrics.total_volume || 0 }
      ]
    : []

  return (
    <div>
      <div className="mb-6 flex flex-col gap-4 md:flex-row">
        <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
          <h2 className="text-xl font-semibold text-slate-100">KPI Marché</h2>
          <p className="mt-4 text-4xl font-bold text-cyan-400">{metrics ? metrics.total_rows : "--"}</p>
          <p className="mt-2 text-slate-400">Enregistrements surveillés</p>
        </div>
        <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
          <h2 className="text-xl font-semibold text-slate-100">Anomalies IA</h2>
          <p className="mt-4 text-4xl font-bold text-rose-400">{metrics ? metrics.ai_anomaly_count : "--"}</p>
          <p className="mt-2 text-slate-400">Transactions suspectes détectées</p>
        </div>
        <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
          <h2 className="text-xl font-semibold text-slate-100">Risque global</h2>
          <p className="mt-4 text-4xl font-bold text-amber-400">{metrics ? metrics.risk_level : "--"}</p>
          <p className="mt-2 text-slate-400">Score de risque estimé</p>
        </div>
      </div>
      {errors && <div className="rounded-3xl bg-rose-950 p-4 text-rose-200">{errors}</div>}
      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
          <h3 className="mb-4 text-xl font-semibold">Performance prix / volume</h3>
          <ResponsiveContainer width="100%" height={320}>
            <LineChart data={chartData}>
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Line type="monotone" dataKey="value" stroke="#38bdf8" strokeWidth={3} />
            </LineChart>
          </ResponsiveContainer>
        </div>
        <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
          <h3 className="mb-4 text-xl font-semibold">Snapshot marché</h3>
          <ResponsiveContainer width="100%" height={320}>
            <BarChart data={chartData}>
              <XAxis dataKey="name" stroke="#94a3b8" />
              <YAxis stroke="#94a3b8" />
              <Tooltip />
              <Bar dataKey="value" fill="#0ea5e9" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}
