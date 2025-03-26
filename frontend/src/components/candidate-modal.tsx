"use client";

import { Button } from "@/components/ui/button";
import { Rating } from "@/components/Rating-Chart";
import { useState } from "react";
import FeedBackDialog from "@/components/FeeadBackDialog";
interface Candidate {
  name: string;
  title: string;
  score: string;
  ExtractSkills: string;
  MatchedSkills: string;
  MissingSkills: string;
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
    ExtractSkills,
    MatchedSkills,
    MissingSkills,
    file,
    summary,
  } = candidate;
  const [open, setOpen] = useState(false);
  function handleClick() {
    // Open the feedback modal
    setOpen(true);
  }

    console.log("candidate : ", ExtractSkills.split(","))
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
              {MatchedSkills &&
              Array.isArray(MatchedSkills) &&
              MatchedSkills.length > 0 ? (
                MatchedSkills.map((skill, index) => (
                  <li key={index} className="flex items-center">
                    <span className="h-2 w-2 rounded-full bg-green-500 mr-2"></span>
                    <span>{skill}</span>
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
              {MissingSkills &&
              Array.isArray(MissingSkills) &&
              MissingSkills.length > 0 ? (
                MissingSkills.map((skill, index) => (
                  <li key={index} className="flex items-center">
                    <span className="h-2 w-2 rounded-full bg-red-500 mr-2"></span>
                    <span>{skill}</span>
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
              {ExtractSkills &&
              Array.isArray(ExtractSkills) &&
              ExtractSkills.length > 0 ? (
                ExtractSkills.map((skill, index) => (
                  <li key={index} className="flex items-center">
                    <span className="h-2 w-2 rounded-full bg-blue-500 mr-2"></span>
                    <span>{skill[0]}</span>
                  </li>
                ))
              ) : (
                <li>No extra skills available</li>
              )}
            </ul>
          </div>

          <div className="flex flex-col gap-4 justify-center mb-8">
            <Rating score={score} />
            <Button
              variant="outline"
              className="flex-1 bg-gray-200 text-gray-800 hover:bg-[#3F788A99]"
            >
              View Resume
            </Button>
            <Button
              variant="outline"
              className="flex-1 bg-gray-200 text-gray-800 hover:bg-[#3F788A99]"
              onClick={handleClick}
            >
              Give Feedback
            </Button>
          </div>

          <div className="mt-auto">
            {/* <Button variant="outline" className="flex-1 bg-gray-200 text-gray-800 hover:bg-gray-300">
              Close
            </Button> */}
          </div>
        </div>
      </div>
      <FeedBackDialog open={open} setOpen={setOpen} candidate={candidate} />
    </div>
  );
}
