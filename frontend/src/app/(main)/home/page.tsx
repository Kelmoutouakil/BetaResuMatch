"use client"

import type React from "react"
import { useState, useEffect } from "react"
import { Search, ArrowRight, Loader } from "lucide-react"
import { useRouter } from "next/navigation"
import { useRecruiter } from "@/Context/RecruiterContext"
import api from "@/lib/axiosInstance"
import { toast } from "sonner"

export default function SearchPage() {
  const { job_description, setJobDescription } = useRecruiter()
  const router = useRouter()
  const [searchQuery, setSearchQuery] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  // Initialize searchQuery from job_description if it exists
  useEffect(() => {
    if (job_description) {
      setSearchQuery(job_description)
    }
  }, [job_description])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!searchQuery.trim()) {
      toast.error("Please enter a job description")
      return
    }

    setIsLoading(true)

    try {
      // Save to context (which should persist to localStorage via the context)
      setJobDescription(searchQuery)

      // Pre-fetch candidates before navigation to ensure data is available
      await api.post("JDupload/", {
        job_description: searchQuery,
        model: "2",
      })

      // Navigate to the chat page
      router.push("/home/chat")
    } catch (error) {
      console.error("Error fetching candidates:", error)
      toast.error("Failed to process your request. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col w-full">
      <nav className="p-4 flex justify-end">{/* You can add navigation items here if needed */}</nav>

      <main className="flex-1 flex flex-col items-center justify-center px-6">
        <div className="w-32 h-32 md:w-40 md:h-40 mb-12 flex items-center justify-center">
          <div className="w-full h-full bg-black rounded-full flex items-center justify-center">
            <span className="text-white text-6xl md:text-7xl">β</span>
          </div>
        </div>

        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-black max-w-5xl mb-8 text-center">
          Welcome to the fastest Hiring AI
        </h1>

        <div className="flex items-center space-x-3 mb-16">
          <Search className="w-6 h-6 text-black" />
          <span className="text-lg md:text-xl font-semibold uppercase text-black">What are you looking for?</span>
        </div>

        <form onSubmit={handleSubmit} className="w-full max-w-3xl">
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Describe the role, required skills, and experience..."
              className="w-full bg-[#2F2E2E] text-white rounded-full py-4 pl-12 pr-16 focus:outline-none focus:ring-2 focus:ring-[#89A8B2]"
              disabled={isLoading}
            />

            <button
              type="submit"
              disabled={isLoading}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 bg-[#89A8B2] rounded-full flex items-center justify-center hover:bg-opacity-90 transition-colors disabled:opacity-70"
            >
              {isLoading ? (
                <Loader className="w-5 h-5 text-white animate-spin" />
              ) : (
                <ArrowRight className="w-5 h-5 text-white" />
              )}
            </button>
          </div>
        </form>
      </main>
    </div>
  )
}

