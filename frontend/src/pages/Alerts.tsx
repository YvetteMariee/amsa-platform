import { useEffect, useState } from "react"
import api from "../services/api"

export default function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([])
  const [error, setError] = useState("")

  useEffect(() => {
    api.get("/alerts")
      .then((response) => setAlerts(response.data))
      .catch(() => setError("Impossible de charger les alertes."))
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-semibold text-slate-100">Alertes détectées</h2>
      {error && <div className="rounded-3xl bg-rose-950 p-4 text-rose-200">{error}</div>}
      <div className="grid gap-4">
        {alerts.length === 0 ? (
          <div className="rounded-3xl bg-slate-900 p-6 text-slate-400">Aucune alerte disponible pour le moment.</div>
        ) : (
          alerts.map((alert) => (
            <div key={alert.id} className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/20">
              <div className="flex flex-wrap items-center justify-between gap-4">
                <div>
                  <p className="text-lg font-semibold text-slate-100">{alert.instrument || "Instrument inconnu"}</p>
                  <p className="text-sm text-slate-400">Statut: {alert.status}</p>
                </div>
                <span className="rounded-full bg-amber-500 px-4 py-2 text-sm font-semibold text-slate-950">
                  {alert.risk_level || "MEDIUM"}
                </span>
              </div>
              <div className="mt-4 text-slate-300">
                Score IA: {alert.anomaly_score ?? "N/A"}
              </div>
              <div className="mt-3 text-sm text-slate-500">Commentaire: {alert.comments || "Aucun"}</div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
