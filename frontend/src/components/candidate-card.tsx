"use client";
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
import CandidateModal from "./candidate-modal";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function CandidateCard({ candidate }: CandidateCardProps) {
  const { name, title, score } = candidate;
  // const [isModalOpen, setIsModalOpen] = useState(false);
  return (
    <Dialog>
      <DialogTrigger className=" w-full lg:w-[380px]">
        <div
          className="relative bg-[#3F788A99] text-black rounded-xl px-4 lg:px-6 py-4 lg:max-w-[380px] transition-transform hover:translate-y-[-2px] flex flex-col gap-2 items-start justify-start"
          // style={{ boxShadow: "5px 5px 17.4px rgba(0, 0, 0, 0.5)" }}
        >
          <div className="absolute top-4 right-6 font-bold  text-lg lg:text-xl">
            {score || 0}%
          </div>
          <h2 className="text-lg lg:text-xl font-semibold mb-1">
            {name || "Can't extract name"}
          </h2>
          <p className="text-black/80">{title || "can't extract job title"}</p>
        </div>
      </DialogTrigger>
      <DialogContent className="w-full max-w-full lg:max-w-[500px] rounded-none lg:rounded-[11px] lg:w-[500px] h-full lg:h-fit  lg:max-h-[70vh] overflow-hidden overflow-y-scroll">
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
  );
}
