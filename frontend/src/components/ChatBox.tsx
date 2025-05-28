import React from 'react';
import { Send } from 'lucide-react';
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem
} from '@/components/ui/select';

interface ChatBoxProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  dropdownValue: string;
  onDropdownChange: (value: string) => void;
  onSend: () => void;
  dropdownOptions: string[];
  abbrMap: Record<string, string>;
  credits: number;
}

const MAX_CHAR = 300;

export const ChatBox: React.FC<ChatBoxProps> = ({
  value,
  onChange,
  dropdownValue,
  onDropdownChange,
  onSend,
  dropdownOptions,
  abbrMap,
  credits,
}) => {
  // temporary disable send button if no credits
  const isDisabled = value.trim().length === 0 || value.length > MAX_CHAR || dropdownValue === "" || credits === 0;

  return (
    <div className="w-full max-w-4xl">
      <div className="relative rounded-xl border border-border bg-background p-8 min-h-[250px] flex flex-col justify-between">
        {/* Character Counter */}
        <span className="absolute top-3 right-5 text-xs text-muted-foreground select-none">
          {value.length}/{MAX_CHAR} characters
        </span>
        {/* Main Content */}
        <div className="flex-1 flex flex-col justify-between">
          {/* Textarea */}
          <textarea
            className="w-full resize-none border-none bg-transparent text-lg focus:ring-0 focus:outline-none placeholder:text-muted-foreground min-h-[80px]"
            maxLength={MAX_CHAR}
            value={value}
            onChange={onChange}
            placeholder="Describe your research interests, e.g., AI + Robotics"
            rows={3}
          />
          {/* Bottom Row: Dropdown left, Buttons right */}
          <div className="flex items-end justify-between mt-6">
            {/* shadcn Select Dropdown */}
            <Select value={dropdownValue} onValueChange={onDropdownChange}>
              <SelectTrigger className="rounded-full min-w-[180px] max-w-[220px] h-9 px-8 py-1.5">
                <SelectValue placeholder="Select school">
                  {dropdownValue && abbrMap[dropdownValue]}
                </SelectValue>
              </SelectTrigger>
              <SelectContent>
                {dropdownOptions.map((option) => (
                  <SelectItem key={option} value={option}>
                    {option}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {/* Buttons */}
            <div className="flex gap-6">
              {/* <button
                type="button"
                onClick={onRerun}
                disabled={isDisabled}
                className="disabled:opacity-40 disabled:cursor-not-allowed p-2 rounded-full hover:bg-muted transition-colors"
                aria-label="Rerun"
              >
                <RefreshCw size={28} />
              </button> */}
              <button
                type="button"
                onClick={onSend}
                disabled={isDisabled}
                className="disabled:opacity-40 disabled:cursor-not-allowed p-2 rounded-full hover:bg-primary/10 transition-colors"
                aria-label="Send"
              >
                <Send size={28} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatBox;
