import { useEffect, useState } from "react"
import api from "../services/api"

export default function Reports() {
  const [reports, setReports] = useState<any[]>([])
  const [error, setError] = useState("")

  useEffect(() => {
    api.get("/reports")
      .then((response) => setReports(response.data.reports || []))
      .catch(() => setError("Impossible de charger les rapports."))
  }, [])

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-semibold text-slate-100">Rapports de supervision</h2>
      {error && <div className="rounded-3xl bg-rose-950 p-4 text-rose-200">{error}</div>}
      {reports.map((report, index) => (
        <div key={index} className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/20">
          <h3 className="text-2xl font-semibold text-slate-100">{report.title}</h3>
          <p className="mt-2 text-slate-400">Période: {report.period}</p>
          <div className="mt-6 space-y-4">
            <h4 className="text-lg font-semibold text-slate-100">Synthèse par compartiment</h4>
            <div className="grid gap-4 md:grid-cols-2">
              {report.summary_by_compartiment?.map((item: any, idx: number) => (
                <div key={idx} className="rounded-3xl bg-slate-800 p-4 text-slate-200">
                  <p className="font-semibold text-cyan-300">{item.compartiment}</p>
                  <p className="text-sm">Prix moyen: {item.avg_price?.toFixed(2)}</p>
                  <p className="text-sm">Prix max: {item.max_price?.toFixed(2)}</p>
                  <p className="text-sm">Volume total: {item.total_volume}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
