"use client";

import type React from "react";
import { useState } from "react";
import { Input, Button, Select } from "antd";
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
}

interface SearchBarProps {
  candidates: Candidate[];
  setCandidates: React.Dispatch<React.SetStateAction<Candidate[]>>;
}
const SearchBar: React.FC<SearchBarProps> = ({ candidates, setCandidates }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterType, setFilterType] = useState<"skills" | "job">("skills");
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = () => {
    if (!searchQuery.trim()) {
      toast.error("Please enter a search query");
      return;
    }

    setIsSearching(true);
    const filteredCandidates = candidates.filter((candidate) => {
      const query = searchQuery.toLowerCase().trim();

      if (filterType === "skills") {
        const extractedSkills = candidate.ExtractSkills.toLowerCase();
        const matchedSkills = candidate.MatchedSkills.toLowerCase();
        return extractedSkills.includes(query) || matchedSkills.includes(query);
      } else if (filterType === "job") {
        return candidate.jobtitle.toLowerCase().includes(query);
      }

      return false;
    });

    setCandidates(filteredCandidates);
    setIsSearching(false);
  };
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSearchQuery(e.target.value);
  };

  const handleFilterTypeChange = (value: "skills" | "job") => {
    setFilterType(value);
  };

  return (
    <div style={{ display: "flex", gap: "10px", marginBottom: "20px" }}>
      <Input
        placeholder="Search"
        value={searchQuery}
        onChange={handleInputChange}
        style={{ width: 300 }}
      />
      <Select
        defaultValue="skills"
        style={{ width: 120 }}
        onChange={handleFilterTypeChange}
        options={[
          { value: "skills", label: "Skills" },
          { value: "job", label: "Job Title" },
        ]}
      />
      <Button
        type="primary"
        icon={<SearchOutlined />}
        onClick={handleSearch}
        loading={isSearching}
      >
        Search
      </Button>
    </div>
  );
};

export default SearchBar;
