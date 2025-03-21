"use client"; // Ensure this component is client-side

import { SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";

export default function SidebarLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="flex h-screen w-full">
    <SidebarProvider>
          <AppSidebar /> 
          {children} 
    </SidebarProvider>
    </div>
  );
}
