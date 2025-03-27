"use client"; 
import LoginForm from "@/components/login-form";
export default function Login() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("crf");
    localStorage.removeItem("first_name");
    localStorage.removeItem("last_name");
  }
  return (
    <div className="flex items-center justify-center w-full h-screen">
        <LoginForm />
    </div>
  );
}
