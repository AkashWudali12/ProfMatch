import React from 'react';
import { Book, Mail } from 'lucide-react';
import { Professor } from '../../types/professor';
// import { on } from 'events';

interface ProfCardProps {
  professor: Professor;
  onGscholarClick: (url: string) => void;
  onEmailClick: () => void;
  emailCopied: boolean;
}

const ProfCard: React.FC<ProfCardProps> = ({ professor, onGscholarClick, onEmailClick, emailCopied }) => {
  return (
    <div className="w-full max-w-5xl border rounded-xl p-6 md:p-8 bg-background flex flex-col gap-4">
      <div className="flex flex-row justify-between items-start gap-4">
        <div>
          <div className="text-3xl font-semibold mb-2">{professor.name}</div>
          <div className="text-lg text-muted-foreground mb-4">{professor.school}</div>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-base text-muted-foreground">{professor.email_address}</span>
            <div className="relative group">
              <button
                onClick={onEmailClick}
                className="p-1 rounded hover:bg-muted transition-colors"
                aria-label="Copy Email"
              >
                <Mail size={20} />
              </button>
              <span className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-10">Copy email</span>
            </div>
            <div className="relative group">
              <button
                onClick={() => onGscholarClick(professor.gscholar)}
                className="p-1 rounded hover:bg-muted transition-colors"
                aria-label="Google Scholar profile"
              >
                <Book size={20} />
              </button>
              <span className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-10">Google Scholar profile</span>
            </div>
          </div>
            {emailCopied && (
              <div className="text-xs text-green-600 mb-2">Email copied to clipboard!</div>
            )}
          </div>
        {/* <div className="flex gap-4">
          <div className="relative group">
            <button
              onClick={() => onGscholarClick(professor.gscholar)}
              className="p-2 rounded hover:bg-muted transition-colors"
              aria-label="Google Scholar profile"
            >
              <Book size={36} />
            </button>
            <span className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-10">Google Scholar profile</span>
          </div>
          <div className="relative group">
            <button
              onClick={onEmailClick}
              className="p-2 rounded hover:bg-muted transition-colors"
              aria-label="Email"
            >
              <Mail size={36} />
            </button>
            <span className="absolute left-1/2 -translate-x-1/2 top-full mt-2 px-2 py-1 rounded bg-black text-white text-xs opacity-0 group-hover:opacity-100 pointer-events-none whitespace-nowrap z-10">Email</span>
          </div> */}
      </div>
      <div className="text-base leading-relaxed whitespace-pre-line">
        {professor.description}
      </div>
    </div>
  );
};

export default ProfCard;
