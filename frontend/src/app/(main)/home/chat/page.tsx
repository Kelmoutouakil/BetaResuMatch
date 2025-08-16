"use client";
import CandidateCard from "@/components/candidate-card";
import SearchBar from "@/components/search-bar";
import { useState } from "react";
import api from "@/lib/axiosInstance";
import { toast } from "sonner";
import { useEffect } from "react";
import { useRecruiter } from "@/Context/RecruiterContext";
import { Button } from "@/components/ui/button";
import { StatisticsDialog } from "@/components/statisticts";
interface Candidate {
  name: string;
  jobtitle: string;
  score: string;
  ExtractSkills: string;
  MatchedSkills: string;
  MissingSkills: string;
  file: string;
  summary: string;
  feedback: string;
}
interface StatisticsData {
  school_data: Record<string, number>;
  job_data: Record<string, number>;
}

export default function Home() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const { module } = useRecruiter();
  const [statisticsOpen, setStatisticsOpen] = useState(false);
  const [statisticsData, setStatisticsData] = useState<StatisticsData | null>(
    null
  );
  useEffect(() => {
    const sendQuery = async () => {
      setIsLoading(true);
      try {
        const response = await api.get("api/Rank");
        setCandidates(response.data);
      } catch (err: any) {
        toast.error(err.response?.data?.message || "Something went wrong!");
      } finally {
        setIsLoading(false);
      }
    };
    sendQuery();
  }, [module]);

  useEffect(() => {
    console.log("Updated Candidates:", candidates);
  }, [candidates]);

  const handleClick = async () => {
    try {
      const response = await api.get("api/dashbord/");
      setStatisticsData(response.data);
      setStatisticsOpen(true);
      toast.success("Statistics generated successfully");
    } catch (err: any) {
      toast.error(err.response?.data?.message || "Something went wrong!");
    }
  };

  return (
    <main className="size-full flex flex-col items-start justify-start">
      <div className="mb-10 w-full">
        <SearchBar  candidates={candidates} setCandidates={setCandidates} />
      </div>

      <div className="w-full h-fit flex flex-row justify-between items-start sm:items-center gap-4 sm:gap-0 pr-3">
      <h1 className="text-2xl font-bold text-slate-800 mb-6 sm:mb-0">Results</h1>
      <Button variant="outline" className="bg-gray-200 text-gray-800 hover:bg-[#3F788A99]" onClick={handleClick}>
        View statistics
      </Button>
    </div>
      {isLoading ? (
        <div className="flex justify-center items-center h-40">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[#89A8B2]"></div>
        </div>
      ) : candidates.length > 0 ? (
        <div className="flex flex-wrap items-center p-2 lg:items-start justify-start  gap-x-4  w-full h-fit overflow-y-scroll gap-y-16">
          {candidates.map((candidate, index) => (
            <CandidateCard key={index} candidate={candidate} />
          ))}
        </div>
      ) : (
        <div className="flex text-center text-gray-500 py-10 w-full">
          No candidates found, Upload Resumes and write the job description to
          get started
        </div>
      )}

      <StatisticsDialog
        open={statisticsOpen}
        onOpenChange={setStatisticsOpen}
        data={statisticsData}
      />
    </main>
  );
}
