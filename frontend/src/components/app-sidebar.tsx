"use client";
import { RiChatNewFill } from "react-icons/ri";
import { IoLogOut } from "react-icons/io5";
import Cookies from "js-cookie";
import { useRecruiter } from "@/Context/RecruiterContext";
import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarFooter,
} from "@/components/ui/sidebar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import ResumeViewer from "./resume-viewer";
import CandidateList from "./Candidates-Header";
import Logout from "./Logout";
const items = [
  {
    title: "New Chat",
    url: "home",
    icon: RiChatNewFill,
  },
];
export function AppSidebar() {
  const { setModule } = useRecruiter();
  return (
    <Sidebar className="bg-transparent">
      <SidebarHeader className="bg-[#3F788A52]">
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuButton>
                  <div className="flex items-center space-x-3">
                    <div className="w-7 h-7 bg-black rounded-full flex items-center justify-center">
                      <span className="text-white text-xl">β</span>
                    </div>
                    <span className="text-black font-bold text-xl">
                      Ask Beta AI
                    </span>
                  </div>
                </SidebarMenuButton>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-[--radix-popper-anchor-width]">
                <DropdownMenuItem>
                  <span onClick={() => {setModule("1")}}>Beta 1</span>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <span onClick={() => {setModule("2")}}>Beta 2</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu className="gap-5">
              <ResumeViewer />
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span className="ml-2 text-lg font-semibold">
                        {item.title}
                      </span>
                    </a>
                  </SidebarMenuButton>
                  <CandidateList />
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <SidebarMenu>
          <SidebarMenuItem>
            <DropdownMenu>
              <div className="ml-2 text-lg font-semibold w-full items-start justify-center mb-3 flex flex-row gap-4">
                  <IoLogOut className="size-[25px]" />
                  <Logout />
              </div>
            </DropdownMenu>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
