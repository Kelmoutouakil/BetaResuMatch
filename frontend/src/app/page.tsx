import { ArrowRight } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="min-h-screen  flex flex-col">
      <nav className="w-full py-6 px-8 md:px-16 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-black rounded-full flex items-center justify-center">
            <span className="text-[#E2E2E2] text-xl">β</span>
          </div>
          <span className="text-black font-bold text-xl">Ask Beta AI</span>
        </div>

        <div className="flex space-x-4">
          <Link
            href="auth/login"
            className="w-[138px] h-[56px] text-[15px] font-bold rounded-full bg-[#2F2E2E] text-[#E2E2E2] hover:bg-gray-700 transition-colors flex items-center justify-center"
          >
            Login
          </Link>
          <Link
            href="auth/Sign-up"
            className="w-[138px] h-[56px] text-[15px] font-bold rounded-full bg-gray-100 text-[#2F2E2E] hover:bg-[#E2E2E2] transition-colors flex items-center justify-center"
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
          href="/Home"
          className="group px-8 py-4 bg-[#2F2E2E] text-[#E2E2E2] rounded-full font-medium text-lg flex items-center space-x-2 hover:bg-gray-700 transition-all shadow-lg hover:shadow-xl"
        >
          <span>Get Started</span>
          <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
        </Link>
      </main>
    </div>
  );
}
