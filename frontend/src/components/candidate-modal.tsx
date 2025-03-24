"use client";

import { Button } from "@/components/ui/button";
import { Rating } from "@/components/Rating-Chart";
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

interface CandidateCardProps {
  candidate: Candidate;
}

export default function CandidateModal({ candidate }: CandidateCardProps) {
  // Destructure the candidate data
  const {
    name,
    title,
    score,
    extractSkills,
    matchedSkills,
    missingSkills,
    file,
    summary,
  } = candidate;
  return (
    <div className="size-full overflow-y-scroll">
      <div className=" text-black rounded-md max-h-screen flex flex-col relative">
        <div className="p-8 flex flex-col h-full">
          <div className="mb-8">
            <h2 className="text-2xl font-bold">{name}</h2>
            <p className="text-gray-500">{title}</p>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Summary</h3>
            <p className="text-gray-500">{summary}</p>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Matched Skills:</h3>
            <ul className="space-y-2">
              {matchedSkills &&
              Array.isArray(matchedSkills) &&
              matchedSkills.length > 0 ? (
                matchedSkills.map((skill, index) => (
                  <li key={index} className="flex items-center">
                    <span className="h-2 w-2 rounded-full bg-green-500 mr-2"></span>
                    <span>{skill}</span> {/* Display the skill */}
                  </li>
                ))
              ) : (
                <li>No matched skills available</li>
              )}
            </ul>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">
              Missing Required Skills:
            </h3>
            <ul className="space-y-2">
              {missingSkills &&
              Array.isArray(missingSkills) &&
              missingSkills.length > 0 ? (
                missingSkills.map((skill, index) => (
                  <li key={index} className="flex items-center">
                    <span className="h-2 w-2 rounded-full bg-red-500 mr-2"></span>
                    <span>{skill}</span> {/* Display the skill */}
                  </li>
                ))
              ) : (
                <li>No missing skills available</li>
              )}
            </ul>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Extra Skills:</h3>
            <ul className="space-y-2">
              {extractSkills &&
              Array.isArray(extractSkills) &&
              extractSkills.length > 0 ? (
                extractSkills.map((skill, index) => (
                  <li key={index} className="flex items-center">
                    <span className="h-2 w-2 rounded-full bg-blue-500 mr-2"></span>
                    <span>{skill}</span> {/* Display the skill */}
                  </li>
                ))
              ) : (
                <li>No extra skills available</li>
              )}
            </ul>
          </div>

          <div className="flex flex-col gap-4 justify-center mb-8">
            <Rating />
            <Button
              variant="outline"
              className="flex-1 bg-gray-200 text-gray-800 hover:bg-[#3F788A99]"
            >
              View Resume
            </Button>
          </div>

          <div className="mt-auto">
            {/* <Button variant="outline" className="flex-1 bg-gray-200 text-gray-800 hover:bg-gray-300">
              Close
            </Button> */}
          </div>
        </div>
      </div>
    </div>
  );
}
