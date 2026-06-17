import { FormEvent, useState } from "react"
import api from "../services/api"

export default function Search() {
  const [keyword, setKeyword] = useState("")
  const [question, setQuestion] = useState("")
  const [results, setResults] = useState<any>(null)
  const [answer, setAnswer] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!keyword.trim()) return
    setLoading(true)
    try {
      const response = await api.get("/search", { params: { keyword } })
      setResults(response.data)
    } catch {
      setResults({ error: "Erreur lors de la recherche." })
    }
    setLoading(false)
  }

  const handleAsk = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!question.trim()) return
    setLoading(true)
    try {
      const response = await api.get("/ask", { params: { question } })
      setAnswer(response.data)
    } catch {
      setAnswer({ answer: "Erreur lors de la requête IA." })
    }
    setLoading(false)
  }

  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-semibold text-slate-100">Recherche & IA</h2>

      <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
        <h3 className="mb-4 text-xl font-semibold">Recherche documentaire</h3>
        <form className="flex gap-4" onSubmit={handleSearch}>
          <input
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            className="flex-1 rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-cyan-500"
            placeholder="Mot-clé..."
          />
          <button className="rounded-2xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400">
            Chercher
          </button>
        </form>
        {results && !results.error && (
          <div className="mt-4 space-y-2">
            <p className="text-slate-400">{results.total_results} résultat(s)</p>
            {results.results?.map((r: any, i: number) => (
              <div key={i} className="rounded-2xl bg-slate-800 p-4 text-sm text-slate-200">
                <p className="font-semibold text-cyan-300">{r.id}</p>
                <p className="mt-1">{r.document?.substring(0, 300)}</p>
              </div>
            ))}
          </div>
        )}
        {results?.error && <p className="mt-4 text-rose-400">{results.error}</p>}
      </div>

      <div className="rounded-3xl bg-slate-900 p-6 shadow-xl shadow-slate-900/30">
        <h3 className="mb-4 text-xl font-semibold">Poser une question (IA)</h3>
        <form className="flex gap-4" onSubmit={handleAsk}>
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            className="flex-1 rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-slate-100 outline-none focus:border-cyan-500"
            placeholder="Votre question sur la réglementation CEMAC..."
          />
          <button className="rounded-2xl bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400">
            Demander
          </button>
        </form>
        {answer && (
          <div className="mt-4 rounded-2xl bg-slate-800 p-4 text-slate-200">
            <p className="font-semibold text-cyan-300 mb-2">Réponse :</p>
            <p>{answer.answer}</p>
            {answer.sources?.length > 0 && (
              <div className="mt-3 text-sm text-slate-400">
                <p className="font-semibold">Sources ({answer.sources.length}) :</p>
                {answer.sources.map((s: string, i: number) => (
                  <p key={i} className="mt-1 truncate">{s.substring(0, 150)}...</p>
                ))}
              </div>
            )}
          </div>
        )}
      </div>

      {loading && <p className="text-slate-400">Chargement...</p>}
    </div>
  )
}
