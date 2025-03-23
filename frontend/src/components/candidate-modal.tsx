"use client";

import { Button } from "@/components/ui/button";
import { Rating } from "@/components/Rating-Chart";

export default function CandidateModal() {
  return (
    <div className="size-full overflow-y-scroll">
      <div className=" text-black rounded-md max-h-screen flex flex-col relative">
        <div className="p-8 flex flex-col h-full">
          <div className="mb-8">
            <h2 className="text-2xl font-bold">Meryeme</h2>
            <p className="text-gray-500">hhhhh</p>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Summary</h3>
            <p className="text-gray-500">
              Lorem ipsum dolor sit amet consectetur. Est mi volutpat metus
              habitant rutrum lobortis ornare viverra. Quam diam egestas diam
              aliquam. Purus cursus habitasse in tristique ultrices maecenas
              gravida praesent. Ullamcorper fames donec turpis pulvinar.
            </p>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Matched Skills:</h3>
            <ul className="space-y-2">
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-green-500 mr-2"></span>
                <span>+3 years Experience</span>
              </li>
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-green-500 mr-2"></span>
                <span>NextJs</span>
              </li>
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-green-500 mr-2"></span>
                <span>ReactJs</span>
              </li>
            </ul>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">
              Missing Required Skills:
            </h3>
            <ul className="space-y-2">
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-red-500 mr-2"></span>
                <span>ThreeJs</span>
              </li>
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-red-500 mr-2"></span>
                <span>MongoDB</span>
              </li>
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-red-500 mr-2"></span>
                <span>Django</span>
              </li>
            </ul>
          </div>

          <div className="mb-8">
            <h3 className="text-xl font-semibold mb-2">Extra Skills:</h3>
            <ul className="space-y-2">
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-black mr-2"></span>
                <span>React native</span>
              </li>
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-black mr-2"></span>
                <span>C++</span>
              </li>
              <li className="flex items-center">
                <span className="h-2 w-2 rounded-full bg-black mr-2"></span>
                <span>Problem-Solving</span>
              </li>
            </ul>
          </div>

          <div className="flex flex-col gap-4 justify-center mb-8">
            <Rating />
              <Button
                variant="outline"
                className="flex-1 bg-gray-200 text-gray-800 hover:bg-[#3F788A99]"
              >
                View Resume
              </Button>
          </div>

          <div className="mt-auto">
            {/* <Button variant="outline" className="flex-1 bg-gray-200 text-gray-800 hover:bg-gray-300">
              Close
            </Button> */}
          </div>
        </div>
      </div>
    </div>
  );
}
