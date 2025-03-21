"use client"; // Ensure this component is client-side

import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

export default function SidebarLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex min-h-screen w-full overflow-hidden">
      <SidebarProvider>
        <AppSidebar />
        <main className="flex-1 overflow-auto">
          <div className="p-4">
            <SidebarTrigger className="mb-4" />
            {children}
          </div>
        </main>
      </SidebarProvider>
    </div>
  );
}