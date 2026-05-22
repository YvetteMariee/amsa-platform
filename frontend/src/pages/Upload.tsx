import { FormEvent, useState } from "react"
import api from "../services/api"

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)
  const [message, setMessage] = useState("")

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!file) {
      setMessage("Veuillez sélectionner un fichier.")
      return
    }

    const form = new FormData()
    form.append("file", file)

    try {
      const response = await api.post("/upload", form, {
        headers: { "Content-Type": "multipart/form-data" }
      })
      setMessage(`Fichier ${response.data.file} ingéré (${response.data.rows || response.data.rows_inserted} lignes).`)
    } catch (err) {
      setMessage("Échec de l'upload. Vérifiez le fichier et réessayez.")
    }
  }

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-semibold text-slate-100">Import de données</h2>
      <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div>
            <label className="block text-sm text-slate-300">Fichier CSV / XLSX / PDF</label>
            <input
              type="file"
              accept=".csv,.xlsx,.xls,.pdf"
              onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              className="mt-2 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100"
            />
          </div>
          <button className="rounded-2xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400">
            Envoyer
          </button>
        </form>
      </div>
      {message && <div className="rounded-3xl bg-slate-800 p-4 text-slate-100">{message}</div>}
    </div>
  )
}
