import ChatBox from "../components/ChatBox";
import React, { useState } from "react";
import { Menu, Pencil } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Professor } from "../types/professor";
import ProfCard from "../components/ProfCard";
import EmailForm from "../components/EmailForm";
import {
  Dialog,
  DialogContent,
  DialogOverlay,
  DialogPortal,
  DialogTrigger,
} from "@/components/ui/dialog";

export default function Home() {
  const [value, setValue] = useState("");
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [dropdownValue, setDropdownValue] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [emailDialogOpen, setEmailDialogOpen] = useState(false);
  const [emailFormData, setEmailFormData] = useState<{
    emailAddress: string;
    subject: string;
    body: string;
  } | null>(null);

  // List of full university names
  const dropdownOptions = [
    "University of Maryland",
    "Massachusetts Institute of Technology",
    "University of California, Berkeley",
  ];

  // Mapping from full name to abbreviation
  const abbrMap: Record<string, string> = {
    "University of Maryland": "UMD",
    "Massachusetts Institute of Technology": "MIT",
    "University of California, Berkeley": "UCB",
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setValue(e.target.value);
  };

  const handleRerun = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  };

  const handleDropdownChange = (value: string) => {
    setDropdownValue(value);
  };

  const handleSend = () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      setProfessors([
        ...professors,
        {
          id: 1,
          uuid: "123",
          name: "John Doe",
          school: "University of Maryland",
          description: "John Doe is a professor at the University of Maryland",
          gscholar: "https://scholar.google.com/citations?user=123",
          email_subject: "Hello",
          email_body: "Hello, how are you?",
          email_address: "john.doe@umd.edu",
        },
        {
          id: 2,
          uuid: "123",
          name: "John Doe",
          school: "University of Maryland",
          description: "John Doe is a professor at the University of Maryland",
          gscholar: "https://scholar.google.com/citations?user=123",
          email_subject: "Hello",
          email_body: "Hello, how are you?",
          email_address: "john.doe@umd.edu",
        },
      ]);
    }, 1000);
  };

  // Dummy handlers for top bar buttons
  const handleSidebar = () => console.log("Sidebar");
  const handleEdit = () => console.log("New Chat");
  const handleLogin = () => console.log("Login");
  const handleSignup = () => console.log("Sign Up");
  const handleLogout = () => console.log("Logout");
  const handleGscholar = (url: string) => {
    window.open(url, "_blank");
  };
  const handleEmail = (prof: Professor) => {
    setEmailFormData({
      emailAddress: prof.email_address,
      subject: prof.email_subject,
      body: prof.email_body,
    });
    setEmailDialogOpen(true);
  };

  const handleCloseEmailForm = () => {
    setEmailDialogOpen(false);
    setEmailFormData(null);
  };

  return (
    <div className="flex flex-col min-h-screen">
      {/* Top Bar */}
      <div className="flex items-center justify-between w-full px-8 py-6">
        <div className="flex items-center gap-4">
          <div className="relative group">
            <button onClick={handleSidebar} className="p-2 rounded hover:bg-muted transition-colors" aria-label="Sidebar">
              <Menu size={32} />
            </button>
            <span className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-10">Open sidebar</span>
          </div>
          <div className="relative group">
            <button onClick={handleEdit} className="p-2 rounded hover:bg-muted transition-colors" aria-label="New Chat">
              <Pencil size={32} />
            </button>
            <span className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-10">New chat</span>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <Button variant="outline" onClick={handleSignup}>Sign Up</Button>
          <Button onClick={handleLogin}>Login</Button>
        </div>
      </div>
      {/* Main Content */}
      <div className="flex flex-col items-center justify-center flex-1">
        <div className="w-full max-w-4xl flex flex-col items-center">
          <ChatBox 
            value={value}
            onChange={handleChange}
            dropdownValue={dropdownValue}
            onDropdownChange={handleDropdownChange}
            onSend={handleSend}
            onRerun={handleRerun}
            dropdownOptions={dropdownOptions}
            abbrMap={abbrMap}
          />
          {professors.length > 0 ? (
            <div className="flex flex-col w-full max-w-4xl gap-8 mt-12">
              {professors.map((professor) => (
                <ProfCard key={professor.id} professor={professor} onGscholarClick={handleGscholar} onEmailClick={() => handleEmail(professor)} />
              ))}
            </div>
          ) : (
            <></>
          )}
        </div>
        {isLoading ? (
          <div className="mt-16 flex items-center space-x-6">
            <span className="dot bg-primary inline-block rounded-full w-6 h-6 animate-bounce [animation-delay:-0.32s]"></span>
            <span className="dot bg-primary inline-block rounded-full w-6 h-6 animate-bounce [animation-delay:-0.16s]"></span>
            <span className="dot bg-primary inline-block rounded-full w-6 h-6 animate-bounce"></span>
          </div>
        ) : (
          <></>
        )}
        <style>{`
          .dot {
            animation-name: bounce;
            animation-duration: 1s;
            animation-iteration-count: infinite;
          }
          @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(0.8); }
          }
        `}</style>
      </div>
      {/* EmailForm Dialog */}
      <Dialog open={emailDialogOpen} onOpenChange={setEmailDialogOpen}>
        <DialogPortal>
          <DialogOverlay className="bg-black/40 fixed inset-0 z-50" />
          <DialogContent className="z-50 flex items-center justify-center">
            {emailFormData && (
              <EmailForm
                emailAddress={emailFormData.emailAddress}
                subject={emailFormData.subject}
                body={emailFormData.body}
                onClose={handleCloseEmailForm}
              />
            )}
          </DialogContent>
        </DialogPortal>
      </Dialog>
    </div>
  );
}