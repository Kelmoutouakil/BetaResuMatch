"use client";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { useRecruiter } from "@/Context/RecruiterContext";
import { useEffect } from "react";
import api from "@/lib/axiosInstance";
import { toast } from "sonner";
import { useState } from "react";

export default function SidebarLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { setFirstName, setLastName } = useRecruiter();
  const [initials, setInitials] = useState<string>("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get("user/getUser");
        const firstName = res.data.first_name;
        const lastName = res.data.last_name;

        setFirstName(firstName);
        setLastName(lastName);
        localStorage.setItem("first_name", firstName);
        localStorage.setItem("last_name", lastName);

        const firstLetter = firstName.charAt(0).toUpperCase();
        const lastLetter = lastName.charAt(0).toUpperCase();
        setInitials(`${firstLetter}${lastLetter}`);
      } catch (err) {
        toast.error("Failed to get user data");
      }
    };

    fetchData();
  }, []);
  return (
    <div className="flex min-h-screen w-full overflow-hidden flex-col">
      <div className="flex flex-1">
        <SidebarProvider>
          <AppSidebar />
          <main className="flex-1 ">
            <div className="size-full p-4 items-start flex flex-col justify-start">
              <div className="w-full h-fit flex items-center justify-between py-3">
                <SidebarTrigger />
                <Avatar className="size-[40px] pr-1">
                  <AvatarFallback>{initials}</AvatarFallback>
                </Avatar>
              </div>

              {children}
            </div>
          </main>
        </SidebarProvider>
      </div>
    </div>
  );
}
