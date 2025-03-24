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
  useEffect(() => {
    console.log("Job Description:", job_description);
    if (job_description) {
      const sendQuery = async () => {
        try {
          const response = await api.post("JDupload/", {
            job_description: job_description,
            model: "2",
          });
          console.log("response : ", response.data);
          setCandidates(response.data);
        } catch (err: any) {
          toast.error(err.response?.data?.message || "Something went wrong!");
        }
      };
      sendQuery();
    }
  }, [job_description]);

  return (
    <main className="min-h-screen p-6 w-full">
      <div className="size-full">
        <div className="mb-10">
          <SearchBar />
        </div>

        <h1 className="text-2xl font-bold text-slate-800 mb-6">Results</h1>

        <div className="flex flex-wrap gap-8 size-full ml-[-25px]">
          {candidates.map((candidate, index) => (
            <CandidateCard key={index} candidate={candidate} />
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
  );
}
