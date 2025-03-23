// import { Search } from "lucide-react";
import { IconAdjustmentsHorizontal } from '@tabler/icons-react';
export default function SearchBar() {
  return (
    <div className="relative w-full max-w-2xl mx-auto ">
      <input
        type="text"
        placeholder="Search by skills, and experience ..."
        className="w-full bg-[#2F2E2E] text-white rounded-full shadow-2xl py-3 px-6 pr-12 focus:outline-none focus:ring-2 focus:ring-[#3F788A]"
      />
      <button className="absolute right-3 top-1/2 transform -translate-y-1/2 bg-[#89A8B2] p-2 rounded-full">
        {/* <Search className="h-5 w-5 text-slate-300" /> */}
        <IconAdjustmentsHorizontal stroke={2} className="h-5 w-5 text-white"/>
      </button>
    </div>
  );
}
