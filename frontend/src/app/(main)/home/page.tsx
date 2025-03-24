"use client";

import type React from "react";
import { useState } from "react";
import { Search, Upload, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import api from "@/lib/axiosInstance";
import { toast } from "sonner";


export default function SearchPage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submitted query:", searchQuery);
    sendQuery(searchQuery);
  };

  const sendQuery = async (query: string) => {
    try {
      await api.post("api/JDupload/", { job_description: query });
      router.push("/home/chat");
      setSearchQuery("");
    } catch (err: any) {
      toast.error(err.response?.data?.message || "Something went wrong!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col w-full">
      <nav>
      </nav>
      <main className="flex-1 flex flex-col items-center justify-center px-6">
        <div className="w-32 h-32 md:w-40 md:h-40 mb-12 flex items-center justify-center">
          <div className="w-full h-full bg-black rounded-full flex items-center justify-center">
            <span className="text-white text-6xl md:text-7xl">β</span>
          </div>
        </div>

        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-black max-w-5xl mb-8 text-center">
          Welcome to the fastest Hiring Ai
        </h1>

        <div className="flex items-center space-x-3 mb-16">
          <Search className="w-6 h-6 text-black" />
          <span className="text-lg md:text-xl font-semibold uppercase text-black">
            What are you looking for ?
          </span>
        </div>

        <form onSubmit={handleSubmit} className="w-full max-w-3xl">
          <div className="relative">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Describe the role, required skills, and experience..."
              className="w-full bg-[#2F2E2E] text-white/50 rounded-full py-4 pl-12 pr-16 focus:outline-none focus:ring-2 focus:ring-[#89A8B2]"
            />

            <button
              type="submit"
              className="absolute right-2 top-1/2 -translate-y-1/2 w-10 h-10 bg-[#89A8B2] rounded-full flex items-center justify-center hover:bg-opacity-90 transition-colors"
            >
              {/* {loading ? ( */}
              {/* // <ArrowRight className="w-5 h-5 text-white" /> ) : (<Loader />)} */}
              <ArrowRight className="w-5 h-5 text-white" />
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
