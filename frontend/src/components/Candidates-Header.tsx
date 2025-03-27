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
const backendUrl = "https://localhost:8000";

export default function CandidateList() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);

  useEffect(() => {
    const fetchCandidates = async () => {
      setIsLoading(true);
      try {
        const response = await api.get("getcandidat/");
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
                  onClick={() => setSelectedFile(candidate.file)}
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

      {selectedFile && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-lg max-w-3xl w-full relative">
            <button
              className="absolute top-2 right-2 text-gray-600 hover:text-gray-900"
              onClick={() => setSelectedFile(null)}
            >
              <X className="w-6 h-6" />
            </button>
            <h2 className="text-xl font-semibold mb-4">Candidate Resume</h2>
            <iframe
              src={"https://127.0.0.1:8000/" + selectedFile}
              className="w-full h-[500px] border"
            ></iframe>
          </div>
        </div>
      )}
    </div>
  );
}
