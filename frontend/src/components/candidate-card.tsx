"use client";
interface CandidateCardProps {
  name: string;
  jobTitle: string;
  score: number;
}
import CandidateModal from "./candidate-modal";
import {
  Dialog,
  DialogContent,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function CandidateCard({
  name,
  jobTitle,
  score,
}: CandidateCardProps) {
  // const [isModalOpen, setIsModalOpen] = useState(false);
  return (
    <>
      <Dialog>
        <DialogTrigger className="w-[500px]">
          <div
            className="relative bg-[#3F788A99] text-black rounded-xl px-6 py-4 max-w-[500px] transition-transform hover:translate-y-[-2px]"
            style={{ boxShadow: "5px 5px 17.4px rgba(0, 0, 0, 0.5)" }}
          >
            <div className="absolute top-4 right-6 font-bold text-xl">
              {score}%
            </div>
            <h2 className="text-xl font-semibold mb-1 pr-16">{name}</h2>
            <p className="text-black/80">{jobTitle}</p>
          </div>
        </DialogTrigger>
        <DialogContent className="max-h-screen">
          <DialogTitle className="text-2xl">Candidate Profile Overview</DialogTitle>
          {/* <DialogDescription> */}
          <CandidateModal />
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
