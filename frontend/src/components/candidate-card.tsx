"use client";
interface Candidate {
  name: string;
  title: string;
  score: string;
  extractSkills: string;
  MatchedSkills: string;
  MissingSkills: string;
  file: string;
  summary: string;
}

interface CandidateCardProps {
  candidate: Candidate;
}
import CandidateModal from "./candidate-modal";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function CandidateCard({ candidate }: CandidateCardProps) {
  // Destructure the candidate data
  const { name, title, score } = candidate;
  // const [isModalOpen, setIsModalOpen] = useState(false);
  return (
    <>
      <Dialog>
        <DialogTrigger className="w-[380px]">
          <div
            className="relative bg-[#3F788A99] text-black rounded-xl px-6 py-4 max-w-[380px] transition-transform hover:translate-y-[-2px] flex flex-col gap-2 items-start justify-start"
            style={{ boxShadow: "5px 5px 17.4px rgba(0, 0, 0, 0.5)" }}
          >
            <div className="absolute top-4 right-6 font-bold text-xl">
              {score || 0}%
            </div>
            <h2 className="text-xl font-semibold mb-1 pr-16">
              {name || "unkown name"}
            </h2>
            <p className="text-black/80">{title || "unkown title"}</p>
          </div>
        </DialogTrigger>
        <DialogContent className="max-h-screen">
          <DialogTitle className="text-2xl">
            Candidate Profile Overview
          </DialogTitle>
          {/* <DialogDescription> */}
          <CandidateModal candidate={candidate} />
          {/* </DialogDescription> */}
        </DialogContent>
        {/* <DialogContent>
          <DialogHeader>
          This action cannot be undone. This will permanently delete your
          account and remove your data from our servers.
          </DialogDescription>
          </DialogHeader>
        </DialogContent> */}
      </Dialog>
    </>
  );
}
