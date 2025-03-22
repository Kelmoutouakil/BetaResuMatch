"use client";
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import Cookies from "js-cookie";

type RecruiterContextType = {
  firstName: string;
  lastName: string;
  isSigned: boolean;
  accessToken: string | null;
  setFirstName: (name: string) => void;
  setLastName: (name: string) => void;
  setIsSigned: (signed: boolean) => void;
  setAccessToken: (token: string | null) => void;
};

const RecruiterContext = createContext<RecruiterContextType | undefined>(undefined);

export const RecruiterProvider = ({ children }: { children: ReactNode }) => {
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");
  const [isSigned, setIsSigned] = useState<boolean>(false);
  const [accessToken, setAccessToken] = useState<string | null>(null);

  useEffect(() => {
    const storedFirstName = localStorage.getItem("first_name");
    const storedLastName = localStorage.getItem("last_name");
    const storedIsSigned = Cookies.get("isSigned");
    const storedAccessToken = localStorage.getItem("accessToken");

    if (storedFirstName) setFirstName(storedFirstName);
    if (storedLastName) setLastName(storedLastName);
    if (storedIsSigned) setIsSigned(storedIsSigned === "true");
    if (storedAccessToken) setAccessToken(storedAccessToken);
  }, []);

  useEffect(() => {
    localStorage.setItem("first_name", firstName);
    localStorage.setItem("last_name", lastName);
    Cookies.set("isSigned", String(isSigned), { expires: 1 });
  }, [firstName, lastName, isSigned]);

  return (
    <RecruiterContext.Provider value={{ 
      firstName, lastName, isSigned, accessToken, 
      setFirstName, setLastName, setIsSigned, setAccessToken 
    }}>
      {children}
    </RecruiterContext.Provider>
  );
};

export const useRecruiter = () => {
  const context = useContext(RecruiterContext);
  if (!context) {
    throw new Error("useRecruiter must be used within a RecruiterProvider");
  }
  return context;
};
