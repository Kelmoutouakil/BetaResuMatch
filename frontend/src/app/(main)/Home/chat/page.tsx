import CandidateCard from "@/components/candidate-card"
import SearchBar from "@/components/search-bar"

// Dummy data for candidates
const candidates = [
  { id: 1, name: "Meryeme Mesbahi", jobTitle: "Full-Stack Developer", score: 89 },
  { id: 2, name: "Alex Johnson", jobTitle: "Frontend Developer", score: 92 },
  { id: 3, name: "Sarah Williams", jobTitle: "Backend Developer", score: 85 },
  { id: 4, name: "David Chen", jobTitle: "DevOps Engineer", score: 78 },
  { id: 5, name: "Priya Patel", jobTitle: "UI/UX Designer", score: 94 },
  { id: 6, name: "Michael Rodriguez", jobTitle: "Mobile Developer", score: 81 },
  { id: 7, name: "Emma Thompson", jobTitle: "Data Scientist", score: 88 },
  { id: 8, name: "Omar Hassan", jobTitle: "Full-Stack Developer", score: 90 },
  { id: 9, name: "Sophia Garcia", jobTitle: "Product Manager", score: 87 },
]

export default function Home() {
  return (
    <main className="min-h-screen p-6 w-full">
      <div className="size-full">
        <div className="mb-10">
          <SearchBar />
        </div>

        <h1 className="text-2xl font-bold text-slate-800 mb-6">Results</h1>

        <div className="flex flex-wrap gap-8 size-full ml-[-25px]">
          {candidates.map((candidate) => (
            <CandidateCard
              key={candidate.id}
              name={candidate.name}
              jobTitle={candidate.jobTitle}
              score={candidate.score}
            />
          ))}
        </div>
{/* 
        <div className="mt-10 flex justify-end gap-2">
          <button className="px-4 py-2 rounded bg-white text-slate-700 hover:bg-slate-100">Previous</button>
          <button className="px-4 py-2 rounded bg-white text-slate-700 hover:bg-slate-100">1</button>
          <button className="px-4 py-2 rounded bg-slate-700 text-white">2</button>
          <button className="px-4 py-2 rounded bg-white text-slate-700 hover:bg-slate-100">3</button>
          <button className="px-4 py-2 rounded bg-white text-slate-700 hover:bg-slate-100">...</button>
          <button className="px-4 py-2 rounded bg-white text-slate-700 hover:bg-slate-100">Next</button>
        </div> */}
      </div>
    </main>
  )
}


