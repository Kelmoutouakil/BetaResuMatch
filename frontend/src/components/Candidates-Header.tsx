"use client";

import { useState, useEffect } from "react";
import api from "@/lib/axiosInstance";
import { Loader, X } from "lucide-react";
import { toast } from "sonner";
import { AxiosError } from "axios";

interface Candidate {
  name: string;
  jobtitle: string;
  Instutut_name: string;
  desired_role: string;
  file: string;
  summary: string;
}
export default function CandidateList() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const backendUrl = "https://localhost:8000";

  useEffect(() => {
    const fetchCandidates = async () => {
      setIsLoading(true);
      try {
        const response = await api.get("api/getcandidat/");
        console.log(response.data.file);
        setCandidates(response.data);
      } catch (err) {
        const axiosError = err as AxiosError<{ message: string }>;
        toast.error(
          axiosError?.response?.data?.message || "Something went wrong!"
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchCandidates();
  }, []);

  return (
    <div className="flex h-fit">
      <div className="w-full">
        <div className="relative">
          {isLoading ? (
            <div className="flex justify-center items-center h-40">
              <Loader className="h-8 w-8 animate-spin text-[#89A8B2]" />
            </div>
          ) : candidates.length === 0 ? (
            <div className="text-black p-6 text-center">
              No candidates found
            </div>
          ) : (
            <ul className="flex items-center justify-center flex-wrap lg:justify-start">
              {candidates.map((candidate, index) => (
                <div
                  key={index}
                  className="py-5 px-8 border-b border-gray-500 cursor-pointer transition-colors w-full"
                  onClick={() => {console.log("hnaaa",candidate.file);
                    window.open(backendUrl + candidate.file)}}
                >
                  <div className="text-black text-md font-medium">
                    {candidate.name}
                  </div>
                </div>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}
