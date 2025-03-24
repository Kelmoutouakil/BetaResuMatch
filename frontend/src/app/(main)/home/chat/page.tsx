"use client";
import CandidateCard from "@/components/candidate-card";
import SearchBar from "@/components/search-bar";
import { useState } from "react";
import api from "@/lib/axiosInstance";
import { toast } from "sonner";
import { useEffect } from "react";
import { useRecruiter } from "@/Context/RecruiterContext";

interface Candidate {
  name: string;
  title: string;
  score: string;
  extractSkills: string[];
  matchedSkills: string[];
  missingSkills: string[];
  file: string;
  summary: string;
}

export default function Home() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const { job_description } = useRecruiter();
  const [isLoading, setIsLoading] = useState(false);
  useEffect(() => {
    console.log("Job Description:", job_description);
    if (job_description) {
      const sendQuery = async () => {
        setIsLoading(true);
        try {
          const response = await api.post("JDupload/", {
            job_description: job_description,
            model: "2",
          });
          console.log("response : ", response.data);
          setCandidates(response.data);
        } catch (err: any) {
          toast.error(err.response?.data?.message || "Something went wrong!");
        } finally {
          setIsLoading(false);
        }
      };
      sendQuery();
    }
  }, [job_description]);

  return (
    <main className="min-h-screen p-6 w-full">
      <div className="size-full">
        <div className="mb-10">
          <SearchBar setCandidates={setCandidates} />
        </div>

        <h1 className="text-2xl font-bold text-slate-800 mb-6">Results</h1>

        {isLoading ? (
          <div className="flex justify-center items-center h-40">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#89A8B2]"></div>
          </div>
        ) : candidates.length > 0 ? (
          <div className="flex flex-wrap gap-8 size-full ml-[-25px]">
            {candidates.map((candidate, index) => (
              <CandidateCard key={index} candidate={candidate} />
            ))}
          </div>
        ) : (
          <div className="text-center text-gray-500 py-10">
            {job_description
              ? "No candidates found"
              : "Please enter a job description to find candidates"}
          </div>
        )}
      </div>
    </main>
  );
}
