"use client";

import { Button } from "@/components/ui/button";
import { Rating } from "@/components/Rating-Chart";
import { useState } from "react";
import FeedBackDialog from "@/components/FeeadBackDialog";

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

interface CandidateCardProps {
  candidate: Candidate;
}

export default function CandidateModal({ candidate }: CandidateCardProps) {
  const {
    name,
    jobtitle,
    score,
    ExtractSkills,
    MatchedSkills,
    MissingSkills,
    file,
    summary,
  } = candidate;
  const backendUrl = "https://localhost";
  // const ExtraformattedString = ExtractSkills.replace(/'/g, '"');
  // const MissingformattedString = MissingSkills.replace(/'/g, '"');
  // const MatchedformattedString = MatchedSkills.replace(/'/g, '"');


  // const ExtraskillsArray = JSON.parse(ExtraformattedString);
  // const MissingskillsArray = JSON.parse(MissingformattedString);
  // const MatchedskillsArray = JSON.parse(MatchedformattedString);
  const ExtraformattedString = (ExtractSkills ?? "").replace(/'/g, '"');
  const MissingformattedString = (MissingSkills ?? "").replace(/'/g, '"');
  const MatchedformattedString = (MatchedSkills ?? "").replace(/'/g, '"');

  let ExtraskillsArray = [];
  let MissingskillsArray = [];
  let MatchedskillsArray = [];

  try {
    ExtraskillsArray = JSON.parse(ExtraformattedString || "[]");
    MissingskillsArray = JSON.parse(MissingformattedString || "[]");
    MatchedskillsArray = JSON.parse(MatchedformattedString || "[]");
  } catch (error) {
    console.error("Error parsing skill strings:", error);
  }
  const [openFeedback, setOpenFeedback] = useState(false);

  return (
    <div className="size-full overflow-y-scroll">
      <div className="text-black rounded-md max-h-screen flex flex-col relative">
        <div className="p-8 flex flex-col h-full">
          <div className="mb-8">
            <h2 className="text-2xl font-bold">{name}</h2>
            <p className="text-gray-500">{jobtitle}</p>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Summary</h3>
            <div className="w-full max-h-[300px] overflow-y-scroll">
              <p className="text-gray-500">{summary}</p>
            </div>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Matched Skills:</h3>
            <ul className="space-y-2">
              {MatchedskillsArray.length > 0 ? (
                MatchedskillsArray.map((skill: string, index: number) => (
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
              {MissingskillsArray.length > 0 ? (
                MissingskillsArray.map((skill: string, index: number) => (
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
            <h3 className="text-xl font-semibold mb-2">Extra Skills:</h3>
            <ul className="space-y-2">
              {ExtraskillsArray.length > 0 ? (
                ExtraskillsArray.map((skill: string, index: number) => (
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

          <div className="flex flex-col gap-4 justify-center mb-8">
            <Rating score={score} />

            <Button
              variant="outline"
              className="flex-1 bg-gray-200 text-gray-800 hover:bg-[#3F788A99]"
              onClick={() => window.open(backendUrl + file)}
            >
              View Resume
            </Button>

            <Button
              variant="outline"
              className="flex-1 bg-gray-200 text-gray-800 hover:bg-[#3F788A99]"
              onClick={() => setOpenFeedback(true)}
            >
              Give Feedback
            </Button>
          </div>
        </div>
      </div>

      <FeedBackDialog
        open={openFeedback}
        setOpen={setOpenFeedback}
        candidate={candidate}
      />
    </div>
  );
}
