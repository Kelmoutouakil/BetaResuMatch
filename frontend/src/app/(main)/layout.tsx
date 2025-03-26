"use client"; // Ensure this component is client-side

import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { useRecruiter } from "@/Context/RecruiterContext";
import { User } from "lucide-react";
export default function SidebarLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const { firstName, lastName } = useRecruiter();
  return (
    <div className="flex min-h-screen w-full overflow-hidden flex-col">
      {/* Hello World Div */}
      <div className="w-full flex justify-end mt-5 px-3">
        <div className="w-fit h-[50px] bg-[#2F2E2E] rounded-2xl flex items-center justify-center p-5 shadow-2xl gap-3">
        <User size="20" color="#FFFF" variant="Broken"/>
          <h1 className="text-sm font-medium text-white">
            {firstName} {lastName}
          </h1>
        </div>
      </div>

      <div className="flex flex-1">
        <SidebarProvider>
          <AppSidebar />
          <main className="flex-1 overflow-auto">
            <div className="p-4 items-start flex justify-between gap-auto">
              <SidebarTrigger className="mb-4" />
              {children}
            </div>
          </main>
        </SidebarProvider>
      </div>
    </div>
  );
}
