"use client"; // Ensure this component is client-side
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { useRecruiter } from "@/Context/RecruiterContext";
import { User } from "iconsax-react";
export default function SidebarLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { firstName, lastName } = useRecruiter();
  return (
    <div className="flex min-h-screen w-full overflow-hidden flex-col">
      <div className="flex flex-1">
        <SidebarProvider>
          <AppSidebar />
          <main className="">
            <div className="size-full p-4 items-start flex flex-col justify-start">
              <div className="w-full h-fit flex items-center justify-between py-3">
                <SidebarTrigger className="" />
                <Avatar className="size-[40px]">
                  <AvatarFallback>CN</AvatarFallback>
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
