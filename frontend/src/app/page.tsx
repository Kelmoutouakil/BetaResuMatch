"use client"
import { ArrowRight } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("crf");
    localStorage.removeItem("first_name");
    localStorage.removeItem("last_name");
  }
  const RequestCrf = async() =>{

    fetch("https://127.0.0.1:8000/user/getcsrf/",{
        method: 'GET'
    })
    .then((response)=>response.json())
    .then((data)=>{
      console.log(data)
      localStorage.setItem("crf",data.crfToken)
        
    })
    .catch((error)=>{
        console.log(error)
    })
  }   
  return (
    <div className="min-h-screen  flex flex-col">
      <nav className="w-full py-6 px-8 md:px-16 flex justify-between items-center">
        <div className="flex items-center md:space-x-3 space-x-1">
          <div className="md:w-10 w-8 md:h-10 h-8 bg-black rounded-full flex items-center justify-center">
            <span className="text-[#E2E2E2] text-xl">β</span>
          </div>
          <span className="text-black font-bold md:text-xl text-sm">Ask Beta AI</span>
        </div>

        <div className="flex space-x-4">
          <Link
            onClick={RequestCrf}
            href="auth/login"
            className="md:w-[138px] w-[90px] md:h-[56px] h-[30px] text-[15px] font-bold rounded-full bg-[#2F2E2E] text-[#E2E2E2] hover:bg-gray-700 transition-colors flex items-center justify-center"
          >
            Login
          </Link>
          <Link
          onClick={RequestCrf}
            href="auth/Sign-up"
            className="md:w-[138px] w-[90px] md:h-[56px] h-[30px] text-[15px] font-bold rounded-full bg-gray-100 text-[#2F2E2E] hover:bg-[#E2E2E2] transition-colors flex items-center justify-center"
          >
            Sign up
          </Link>
        </div>
      </nav>

      <main className="flex-1 flex flex-col items-center justify-center px-6 text-center">
        <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-gray-900 max-w-5xl mb-8">
          Welcome to the fastest Hiring Ai
        </h1>

        <p className="text-xl md:text-2xl text-[#2F2E2E] max-w-3xl mb-16">
          Find the perfect candidate in seconds—upload a resume, add a job
          description, and let AI do the rest!
        </p>

        <Link
          href="/auth/Sign-up"
          className="group px-8 py-4 bg-[#2F2E2E] text-[#E2E2E2] rounded-full font-medium text-lg flex items-center space-x-2 hover:bg-gray-700 transition-all shadow-lg hover:shadow-xl"
        >
          <span>Get Started</span>
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </Link>
      </main>
    </div>
  );
}
