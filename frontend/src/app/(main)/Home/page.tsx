"use client";

import type React from "react";

import { useState } from "react";
import Link from "next/link";
import { Search, Upload, ArrowRight } from "lucide-react";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";

export default function SearchPage() {
  const [searchQuery, setSearchQuery] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Submitted query:", searchQuery);
  };
  const [files, setFiles] = useState<FileList | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setFiles(event.target.files);
      console.log([...event.target.files]);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <nav className="w-full py-6 px-8 md:px-16 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-black rounded-full flex items-center justify-center">
            <span className="text-white text-xl">β</span>
          </div>
          <span className="text-black font-bold text-xl">Ask Beta AI</span>
        </div>
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
            {/* <div className="absolute left-4 top-1/2 -translate-y-1/2">
              <label className=" cursor-pointer">
                <Upload className="w-5 h-5 text-white/50" />
                <input
                  type="file"
                  multiple
                  className="hidden"
                  onChange={handleFileChange}
                />
              </label>
            </div> */}

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
              <ArrowRight className="w-5 h-5 text-white" />
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
