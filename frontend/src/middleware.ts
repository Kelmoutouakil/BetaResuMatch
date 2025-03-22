import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(req: NextRequest) {
  const isSigned = req.cookies.get("isSigned")?.value === "true";
  
  const protectedRoutes = ["/home"];
  
  if (protectedRoutes.includes(req.nextUrl.pathname) && !isSigned) {
    return NextResponse.redirect(new URL("/auth/login", req.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/home"],
};
