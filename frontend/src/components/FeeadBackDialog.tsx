"use client";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { DrawerFooter } from "@/components/ui/drawer";
import { Input } from "./ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Loader } from "lucide-react";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import api from "@/lib/axiosInstance";

interface Candidate {
  name: string;
  file: string;
  feedback: string;
}
interface StatisticsDialogProps {
  open: boolean;
  setOpen: (open: boolean) => void;
  candidate: Candidate;
  setCurrentScore: (score: string) => void;
}

export default function FeedBackDialog({
  open,
  setOpen,
  candidate,
  setCurrentScore,
}: StatisticsDialogProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [score, setScore] = useState("");
  const [feedback, setFeedback] = useState("");

  async function handleClick() {
    if (!score.trim() && !feedback.trim()) {
      toast.error("Please enter a score or feedback.");
      return;
    }

    setIsLoading(true);

    try {
      if (score.trim()) {
        await api.post("api/update/", {
          name: candidate.name,
          file: candidate.file,
          score: score,
        });
        setCurrentScore(score);
        toast.success("Score updated successfully!");
      }

      if (feedback.trim()) {
        console.log("feedback : ", feedback);
        const res = await api.post("api/feedback/", {
          name: candidate.name,
          file: candidate.file,
          feedback: feedback,
        });
        toast.success("Feedback submitted successfully!");
      }

      setOpen(false);
    } catch (error: any) {
      toast.error("Failed to submit. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogContent className="sm:max-w-[650px] p-0 border-0">
        <DialogHeader className="p-6 pb-2">
          <DialogTitle className="text-xl font-bold">
            Give your feedback or edit the Rating
          </DialogTitle>
        </DialogHeader>
        <div className="p-6 gap-5 flex flex-col">
          <Label htmlFor="score">Edit score</Label>
          <input
            id="score"
            type="number"
            placeholder="Enter the rating"
            className="w-full border-2 h-[50px] p-3 rounded-xl"
            value={score}
            onChange={(e) => setScore(e.target.value)}
          />
          <Label htmlFor="feedback">Give feedback</Label>
          <input
            id="feedback"
            type="text"
            placeholder={candidate.feedback}
            className="w-full h-[100px] border-2 p-3 rounded-xl"
            value={candidate.feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />
        </div>
        <DrawerFooter className="flex flex-row justify-end">
          <Button variant="outline" onClick={() => setOpen(false)}>
            Close
          </Button>
          <Button onClick={handleClick} disabled={isLoading}>
            {isLoading ? (
              <Loader className="w-5 h-5 text-white animate-spin" />
            ) : (
              "Submit"
            )}
          </Button>
        </DrawerFooter>
      </DialogContent>
    </Dialog>
  );
}
