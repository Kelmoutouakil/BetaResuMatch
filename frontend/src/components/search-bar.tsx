"use client";

import type React from "react";

import { useState } from "react";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import api from "@/lib/axiosInstance";
import { toast } from "sonner";

// Define the Candidate interface if it's not imported from elsewhere
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

interface SearchBarProps {
  setCandidates: React.Dispatch<React.SetStateAction<Candidate[]>>;
}

export default function SearchBar({ setCandidates }: SearchBarProps) {
  const [showFilter, setShowFilter] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState("skills");
  const [isSearching, setIsSearching] = useState(false);

  function handleClick() {
    setShowFilter(!showFilter);
  }

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      toast.error("Please enter a search query");
      return;
    }

    setIsSearching(true);
    try {
      let apiEndpoint = "";
      let requestData = {};

      if (filterType === "skills") {
        apiEndpoint = "filter/";
        requestData = { skill: searchQuery };
      } else if (filterType === "job") {
        apiEndpoint = "filterJob/";
        requestData = { jobtitle: searchQuery };
      } else {
        toast.error("Invalid filter type");
        return;
      }

      const res = await api.post(apiEndpoint, requestData);
      setCandidates(res.data);
    } catch (error) {
      console.error("Error while making search request:", error);
      toast.error("Failed to search candidates");
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="relative w-full max-w-2xl mx-auto">
      <input
        type="text"
        placeholder="Search by skills, and experience ..."
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={isSearching}
        className="w-full bg-[#2F2E2E] text-white rounded-full shadow-2xl py-3 px-6 pr-12 focus:outline-none focus:ring-2 focus:ring-[#3F788A]"
      />

      <Popover open={showFilter} onOpenChange={setShowFilter}>
        <PopoverTrigger asChild>
          <button
            className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-[#89A8B2] p-2 rounded-full"
            onClick={handleClick}
            disabled={isSearching}
          >
            <IconAdjustmentsHorizontal
              stroke={2}
              className="h-5 w-5 text-white"
            />
          </button>
        </PopoverTrigger>
        <PopoverContent
          className="w-56 bg-[#2F2E2E] border border-[#3F788A] text-white p-4 rounded-lg shadow-xl"
          align="end"
        >
          <div className="space-y-4">
            <h3 className="font-medium text-[#89A8B2]">Filter Search By</h3>

            <RadioGroup
              value={filterType}
              onValueChange={setFilterType}
              className="space-y-2"
            >
              <div className="flex items-center space-x-2">
                <RadioGroupItem
                  value="skills"
                  id="skills"
                  className="border-[#89A8B2] text-[#89A8B2]"
                />
                <Label htmlFor="skills" className="text-white">
                  Skills
                </Label>
              </div>

              <div className="flex items-center space-x-2">
                <RadioGroupItem
                  value="job"
                  id="job"
                  className="border-[#89A8B2] text-[#89A8B2]"
                />
                <Label htmlFor="job" className="text-white">
                  Job
                </Label>
              </div>
            </RadioGroup>

            <div className="flex justify-between pt-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowFilter(false)}
                className="bg-transparent border-[#89A8B2] text-white hover:bg-[#3F788A] hover:text-white"
              >
                Cancel
              </Button>
              <Button
                size="sm"
                onClick={() => {
                  handleSearch();
                  setShowFilter(false);
                }}
                className="bg-[#89A8B2] text-white hover:bg-[#3F788A]"
              >
                Apply
              </Button>
            </div>
          </div>
        </PopoverContent>
      </Popover>
    </div>
  );
}

function IconAdjustmentsHorizontal({
  stroke = 1.5,
  className = "",
  ...props
}: {
  stroke?: number;
  className?: string;
  [key: string]: any;
}) {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={stroke}
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      {...props}
    >
      <path d="M4 10h16M4 14h16M8 4v16M16 4v16" />
    </svg>
  );
}
