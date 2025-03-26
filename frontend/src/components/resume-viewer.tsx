"use client";

import type React from "react";
import api from "@/lib/axiosInstance";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  Drawer,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger,
} from "@/components/ui/drawer";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";
import { toast } from "sonner";
import { ChevronLeft, ChevronRight, FileText, Upload, X } from "lucide-react";
import { useMediaQuery } from "@/hooks/use-media-query";
import { Loader } from "lucide-react";

export default function ResumeViewer() {
  const [resumes, setResumes] = useState<File[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const isDesktop = useMediaQuery("(min-width: 768px)");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files).filter(
        (file) =>
          file.type === "application/pdf" ||
          file.type === "application/msword" ||
          file.type ===
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
      );

      if (newFiles.length !== Array.from(e.target.files).length) {
        toast.error("Invalid file type");
      }

      setResumes((prev) => [...prev, ...newFiles]);
    }
  };

  const removeResume = (index: number) => {
    setResumes((prev) => {
      const newResumes = [...prev];
      newResumes.splice(index, 1);
      return newResumes;
    });

    if (currentIndex >= index && currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };

  const nextResume = () => {
    if (currentIndex < resumes.length - 1) {
      setCurrentIndex((prev) => prev + 1);
    }
  };

  const prevResume = () => {
    if (currentIndex > 0) {
      setCurrentIndex((prev) => prev - 1);
    }
  };
  const handleClick = async () => {
    setIsLoading(true);
    try {
      const formData = new FormData();
      for (let i = 0; i < resumes.length; i++) {
        formData.append("files", resumes[i]);
      }
      await api.post("upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      toast.success("Files uploaded successfully");
      setOpen(false);
    } catch (err: any) {
      toast.error("Can't upload files");
    } finally {
      setIsLoading(false);
    }
  };

  if (isDesktop) {
    return (
      <Dialog open={open} onOpenChange={setOpen}>
        <DialogTrigger asChild className="mt-5">
          <Button className="gap-2">
            <Upload className="h-4 w-4" />
            Upload Resumes
          </Button>
        </DialogTrigger>
        <DialogContent className="sm:max-w-[500px]">
          <DialogHeader>
            <DialogTitle>Resume Viewer</DialogTitle>
            <DialogDescription>
              Upload resumes and review them one by one.
            </DialogDescription>
          </DialogHeader>

          <div className="flex flex-col gap-4 my-4">
            <div className="flex items-center gap-2">
              <Input
                id="resume-upload"
                type="file"
                accept=".pdf,.doc,.docx"
                multiple
                onChange={handleFileChange}
                className="flex-1"
              />
              <Label htmlFor="resume-upload" className="sr-only">
                Upload Resumes
              </Label>
            </div>

            {resumes.length > 0 ? (
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <div className="text-sm text-muted-foreground">
                    Viewing {currentIndex + 1} of {resumes.length}
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={prevResume}
                      disabled={currentIndex === 0}
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="icon"
                      onClick={nextResume}
                      disabled={currentIndex === resumes.length - 1}
                    >
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>

                <Card>
                  <CardContent className="p-4">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <FileText className="h-5 w-5 text-primary" />
                        <span className="font-medium">
                          {resumes[currentIndex].name}
                        </span>
                      </div>
                      <Button
                        variant="ghost"
                        size="icon"
                        onClick={() => removeResume(currentIndex)}
                        aria-label="Delete resume"
                      >
                        <X className="h-4 w-4" />
                      </Button>
                    </div>
                  </CardContent>
                </Card>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center gap-4 py-12 text-center border-2 border-dashed rounded-lg">
                <FileText className="h-12 w-12 text-muted-foreground" />
                <div>
                  <p className="text-lg font-medium">No resumes uploaded</p>
                  <p className="text-sm text-muted-foreground">
                    Upload PDF or Word documents to review them
                  </p>
                </div>
              </div>
            )}
          </div>

          <DialogFooter>
            <Button variant="outline" onClick={() => setOpen(false)}>
              Close
            </Button>
            {resumes.length > 0 && (
              <Button onClick={handleClick}>
                {isLoading ? (
                  <Loader className="w-5 h-5 text-white animate-spin" />
                ) : (
                  "Save Selection"
                )}
              </Button>
            )}
          </DialogFooter>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Drawer open={open} onOpenChange={setOpen}>
      <DrawerTrigger asChild>
        <Button className="gap-2">
          <Upload className="h-4 w-4" />
          Upload Resumes
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Resume Viewer</DrawerTitle>
          <DrawerDescription>
            Upload resumes and review them one by one.
          </DrawerDescription>
        </DrawerHeader>

        <div className="px-4 flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <Input
              id="resume-upload-mobile"
              type="file"
              accept=".pdf,.doc,.docx"
              multiple
              onChange={handleFileChange}
              className="flex-1"
            />
            <Label htmlFor="resume-upload-mobile" className="sr-only">
              Upload Resumes
            </Label>
          </div>

          {resumes.length > 0 ? (
            <div className="flex flex-col gap-4">
              <div className="flex items-center justify-between">
                <div className="text-sm text-muted-foreground">
                  Viewing {currentIndex + 1} of {resumes.length}
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={prevResume}
                    disabled={currentIndex === 0}
                  >
                    <ChevronLeft className="h-4 w-4" />
                  </Button>
                  <Button
                    variant="outline"
                    size="icon"
                    onClick={nextResume}
                    disabled={currentIndex === resumes.length - 1}
                  >
                    <ChevronRight className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <FileText className="h-5 w-5 text-primary" />
                      <span className="font-medium truncate max-w-[200px]">
                        {resumes[currentIndex].name}
                      </span>
                    </div>
                    <Button
                      variant="ghost"
                      size="icon"
                      onClick={() => removeResume(currentIndex)}
                      aria-label="Delete resume"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center gap-4 py-8 text-center border-2 border-dashed rounded-lg">
              <FileText className="h-10 w-10 text-muted-foreground" />
              <div>
                <p className="font-medium">No resumes uploaded</p>
                <p className="text-sm text-muted-foreground">
                  Upload PDF or Word documents
                </p>
              </div>
            </div>
          )}
        </div>

        <DrawerFooter>
          <Button variant="outline" onClick={() => setOpen(false)}>
            Close
          </Button>
          {resumes.length > 0 && (
            <Button onClick={handleClick}>Save Selection</Button>
          )}
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  );
}
