"use client"

import { useState, useEffect } from "react"
import api from "@/lib/axiosInstance"
import { Loader } from "lucide-react"
import { toast } from "sonner"

interface Candidate {
  name: string
  jobtitle: string
  Instutut_name: string
  desired_role: string
  file: string
  summary: string
}

export default function CandidateList() {
  const [candidates, setCandidates] = useState<Candidate[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [selectedCandidate, setSelectedCandidate] = useState<Candidate | null>(null)

  useEffect(() => {
    const fetchCandidates = async () => {
      setIsLoading(true)
      try {
        const response = await api.get("getcandidat/")
        console.log("response : ", response.data)
        setCandidates(response.data)
      } catch (err) {
        toast.error(err.response?.data?.message || "Something went wrong!")
      } finally {
        setIsLoading(false)
      }
    }

    fetchCandidates()
  }, [])

  const handleSelectCandidate = (candidate: Candidate) => {
    setSelectedCandidate(candidate)
  }

  return (
    <div className="flex h-fit">
      {/* Left panel - Candidate list */}
      <div className="w-full ">
        <div className="relative">
          {/* Blue accent line */}
          {/* <div className="absolute left-0 top-0 bottom-0 w-1 bg-[#3F788A]"></div> */}

          {isLoading ? (
            <div className="flex justify-center items-center h-40">
              <Loader className="h-8 w-8 animate-spin text-[#89A8B2]" />
            </div>
          ) : candidates.length === 0 ? (
            <div className="text-white p-6 text-center">No candidates found</div>
          ) : (
            <ul className="flex items-center justify-center flex-wrap lg:justify-start">
              {candidates.map((candidate, index) => (
                <li
                  key={index}
                  onClick={() => handleSelectCandidate(candidate)}
                  className={`py-6 px-4 border-b border-gray-700 cursor-pointer hover:bg-[#3F3F3F] transition-colors ${
                    selectedCandidate === candidate ? "bg-[#3F3F3F]" : ""
                  }`}
                >
                  <div className="text-white text-lg font-medium">
                    {candidate.name} - {candidate.jobtitle}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  )
}

