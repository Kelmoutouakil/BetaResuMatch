"use client";

import type React from "react";
import { useState } from "react";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Button } from "@/components/ui/button";
import { SearchOutlined } from "@ant-design/icons";
import { toast } from "react-toastify";

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

interface SearchBarProps {
  setCandidates: React.Dispatch<React.SetStateAction<Candidate[]>>;
  candidates: Candidate[];
}

export default function SearchBar({
  setCandidates,
  candidates,
}: SearchBarProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState<"skills" | "job">("skills");
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      toast.error("Please enter a search query");
      return;
    }
    setIsSearching(true);
    try {
      const query = searchQuery.toLowerCase().trim();

      const filteredCandidates = candidates.filter((candidate) => {
        if (filterType === "skills") {
          const extractedSkills = candidate.ExtractSkills?.toLowerCase() || "";
          const matchedSkills = candidate.MatchedSkills?.toLowerCase() || "";
          return (
            extractedSkills.includes(query) || matchedSkills.includes(query)
          );
        } else if (filterType === "job") {
          console.log("Job Title:", candidate.jobtitle);
          return candidate.jobtitle?.toLowerCase().includes(query);
        }
        return false;
      });
      console.log("Filtered Candidates:", filteredCandidates);

      setCandidates(filteredCandidates);
    } catch (error) {
      toast.error("Error filtering candidates");
      console.error(error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterTypeChange = (value: "skills" | "job") => {
    setFilterType(value);
  };

  return (
    <div className="flex gap-4 mt-5 justify-end">
      <Input
        placeholder="Search"
        value={searchQuery}
        onChange={handleInputChange}
        style={{ width: 300 }}
      />
      <Select>
        <SelectTrigger className="w-[80px]">
          <SelectValue placeholder="Skills"/>
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="job" onClick={() => {handleFilterTypeChange("job")}}>job</SelectItem>
          <SelectItem value="skills" onClick={() => {handleFilterTypeChange("skills")}}>skills</SelectItem>
        </SelectContent>
      </Select>
      <Button onClick={handleSearch} className="bg-gray-200 text-gray-800 hover:bg-[#3F788A99]">Search</Button>
    </div>
  );
}
