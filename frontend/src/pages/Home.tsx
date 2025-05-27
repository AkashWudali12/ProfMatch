import ChatBox from "../components/ChatBox";
import React, { useState } from "react";
import { Copy, Menu, Pencil } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Professor } from "../../types/professor";
import ProfCard from "../components/ProfCard";
import EmailForm from "../components/EmailForm";
import {
  Dialog,
  DialogContent,
  DialogOverlay,
  DialogPortal,
} from "@/components/ui/dialog";

export default function Home() {
  const [value, setValue] = useState<string>("");
  const [professors, setProfessors] = useState<Professor[]>([]);
  const [dropdownValue, setDropdownValue] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [emailDialogOpen, setEmailDialogOpen] = useState<boolean>(false);
  const [emailFormData, setEmailFormData] = useState<{
    emailAddress: string;
    subject: string;
    body: string;
  } | null>(null);
  const [emailCopied, setEmailCopied] = useState<boolean>(false);
  
  // Function to calculate localStorage size in bytes
  const getLocalStorageSize = () => {
    let total = 0;
    Object.keys(localStorage).forEach(key => {
      total += localStorage[key].length + key.length;
    });
    return total;
  };

  // Function to check and reset if localStorage exceeds 2MB
  const checkAndResetStorage = () => {
    const sizeInBytes = getLocalStorageSize();
    const sizeInMB = sizeInBytes / (1024 * 1024);
    
    if (sizeInMB > 2) {
      // Reset to defaults when exceeding 2MB
      localStorage.setItem('dailyCredits', '5');
      localStorage.setItem('previousProfessors', JSON.stringify([]));
      localStorage.setItem('lastResetDate', new Date().toDateString());
      console.log(`localStorage reset: ${sizeInMB.toFixed(2)}MB exceeded 2MB limit`);
      return true; // Indicates reset occurred
    }
    return false;
  };

  const [credits, setCredits] = useState(() => {
    // Check storage capacity first
    const wasReset = checkAndResetStorage();
    if (wasReset) return 5;
    
    // Check if it's a new day
    const today = new Date().toDateString();
    const lastReset = localStorage.getItem('lastResetDate');
    
    if (lastReset !== today) {
      // New day - reset to 5 credits
      localStorage.setItem('dailyCredits', '5');
      localStorage.setItem('lastResetDate', today);
      return 5;
    } else {
      // Same day - use stored credits
      return parseInt(localStorage.getItem('dailyCredits') || '5');
    }
  });

  const [previousProfessors, setPreviousProfessors] = useState(() => {
    // Check storage capacity first
    checkAndResetStorage();
    
    // Same day - use stored list
    const stored = localStorage.getItem('previousProfessors');
    return stored ? JSON.parse(stored) : [];
    
  });

  // List of full university names
  const dropdownOptions = [
    "University of Maryland",
  ];

  // Mapping from full name to abbreviation
  const abbrMap: Record<string, string> = {
    "University of Maryland": "UMD",
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

  const handleSend = async () => {
    setIsLoading(true);
    const queryProfessorsUrl = import.meta.env.VITE_QUERY_PROFESSORS_URL;
    const response = await fetch(queryProfessorsUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ 
        prompt: value, 
        school: dropdownValue, 
        resume_embedding: [], 
        previous_professors: previousProfessors 
      }),
    })
    if (response.ok) {  
      // consume a credit
      const newCredits = credits - 1;
      setCredits(newCredits);
      localStorage.setItem('dailyCredits', newCredits.toString());

      // get professors
      const data = await response.json();
      console.log("data: ", data);
      if (data.professors) {
        setProfessors(data.professors);
        
        // Store returned professor UUIDs (limit to 50 total)
        const newProfessorUUIDs = data.professors.map((prof: Professor) => prof.uuid);
        const updatedPreviousProfessors = [...previousProfessors, ...newProfessorUUIDs].slice(-50); // Keep only last 50
        setPreviousProfessors(updatedPreviousProfessors);
        localStorage.setItem('previousProfessors', JSON.stringify(updatedPreviousProfessors));
      } else {
        console.error("Failed to query professors");
      }
    } else {
      console.error("Failed to query professors");
    }
    setIsLoading(false);
  };

  // Dummy handlers for top bar buttons
  const handleSidebar = () => console.log("Sidebar");
  const handleEdit = () => console.log("New Chat");
  const handleLogin = () => console.log("Login");
  const handleSignup = () => console.log("Sign Up");
  // const handleLogout = () => console.log("Logout");
  const handleGscholar = (url: string) => {
    window.open(url, "_blank");
  };
  const handleEmail = (prof: Professor) => {
    // Copy email to clipboard
    navigator.clipboard.writeText(prof.email_address);
    console.log(`Copied ${prof.email_address} to clipboard`);
    setEmailCopied(true);
    setTimeout(() => setEmailCopied(false), 2000);
    
    /* Commented out email dialog functionality
    setEmailFormData({
      emailAddress: prof.email_address,
      subject: prof.email_subject,
      body: prof.email_body,
    });
    setEmailDialogOpen(true);
    */
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
          {/* <div className="relative group">
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
          </div> */}
          <div className="px-3 py-1 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-full">
            <span className="text-sm font-medium text-blue-700">{credits} credits remaining</span>
          </div>

        </div>
        {/* <div className="flex items-center gap-4">
          <Button variant="outline" onClick={handleSignup}>Sign Up</Button>
          <Button onClick={handleLogin}>Login</Button>
        </div> */}
      </div>
      {/* Main Content */}
      <div className="flex flex-col items-center justify-center flex-1">
        <div className="w-full max-w-4xl flex flex-col items-center">
          {/* ProfMatch Logo */}
          <div className="mb-6 flex flex-col items-center">
            <span className="text-4xl font-extrabold tracking-tight text-primary drop-shadow-sm" style={{ letterSpacing: '0.04em' }}>
              Prof
              <span className="text-white bg-primary px-2 py-1 rounded shadow-md ml-1" style={{
                color: 'white',
                background: 'var(--color-primary, #1d4ed8)',
                boxShadow: '0 2px 8px rgba(0,0,0,0.10)'
              }}>
                Match
              </span>
            </span>
            <span className="text-base text-muted-foreground font-medium mt-1">Find your next research opportunity</span>
            <div className="mt-2 px-3 py-1 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-full">
              <span className="text-sm font-medium text-blue-700">Open Beta – Enjoy 5 Free Credits Every Day!</span>
            </div>
          </div>
          <ChatBox 
            value={value}
            onChange={handleChange}
            dropdownValue={dropdownValue}
            onDropdownChange={handleDropdownChange}
            onSend={handleSend}
            onRerun={handleRerun}
            dropdownOptions={dropdownOptions}
            abbrMap={abbrMap}
            credits={credits}
          />
          {professors.length > 0 ? (
            <div className="flex flex-col w-full max-w-4xl gap-8 mt-12">
              {professors.map((professor) => (
                <ProfCard key={professor.id} professor={professor} onGscholarClick={handleGscholar} onEmailClick={() => handleEmail(professor)} emailCopied={emailCopied} />
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
      {/* Contact Us Section */}
      <div className="w-full bg-muted/30 border-t border-border mt-auto">
        <div className="max-w-4xl mx-auto px-8 py-6">
          <div className="text-center">
            <h3 className="text-lg font-semibold mb-3">Contact Us</h3>
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <span>📧</span>
                <a href="mailto:awudali@terpmail.umd.edu" className="hover:text-primary transition-colors">
                  awudali@terpmail.umd.edu
                </a>
              </div>
              <div className="flex items-center gap-2">
                <span>📞</span>
                <a href="tel:+15714906951" className="hover:text-primary transition-colors">
                  (571) 490-6951
                </a>
              </div>
            </div>
          </div>
        </div>
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