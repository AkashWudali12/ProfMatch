import React, { useRef, useState } from 'react';
import { Button } from "../src/components/ui/button";

interface EmailFormProps {
  emailAddress: string;
  subject: string;
  body: string;
  onClose: () => void;
}

const EmailForm: React.FC<EmailFormProps> = ({ emailAddress, subject, body }) => {
  const emailRef = useRef<HTMLInputElement>(null);
  const subjectRef = useRef<HTMLInputElement>(null);
  const bodyRef = useRef<HTMLTextAreaElement>(null);
  const [copied, setCopied] = useState<string | null>(null);

  const handleCopy = (ref: React.RefObject<HTMLInputElement | HTMLTextAreaElement | null>, label: string) => {
    if (ref.current) {
      navigator.clipboard.writeText(ref.current.value);
    } else {
      navigator.clipboard.writeText('');
    }
    setCopied(label);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <div className="w-full max-w-2xl border rounded-2xl bg-background p-8 relative">
      {/* Email Address */}
      <div className="mb-6">
        <label className="block text-lg font-medium mb-2">Email Address</label>
        <input
          ref={emailRef}
          type="text"
          defaultValue={emailAddress}
          className="w-full rounded-2xl border px-4 py-3 text-base bg-background focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>
      {/* Subject */}
      <div className="mb-6">
        <label className="block text-lg font-medium mb-2">Subject</label>
        <input
          ref={subjectRef}
          type="text"
          defaultValue={subject}
          className="w-full rounded-2xl border px-4 py-3 text-base bg-background focus:outline-none focus:ring-2 focus:ring-primary"
        />
      </div>
      {/* Body */}
      <div className="mb-6">
        <label className="block text-lg font-medium mb-2">Body</label>
        <textarea
          ref={bodyRef}
          defaultValue={body}
          rows={10}
          className="w-full rounded-2xl border px-4 py-3 text-base bg-background focus:outline-none focus:ring-2 focus:ring-primary resize-none"
        />
      </div>
      {/* Copy Buttons */}
      <div className="flex flex-col md:flex-row gap-4 justify-center mt-6">
        <Button variant="outline" onClick={() => handleCopy(emailRef, 'Email Address')} className="flex-1">Copy Email Address</Button>
        <Button variant="outline" onClick={() => handleCopy(subjectRef, 'Subject')} className="flex-1">Copy Subject</Button>
        <Button variant="outline" onClick={() => handleCopy(bodyRef, 'Email Body')} className="flex-1">Copy Email</Button>
      </div>
      {copied && (
        <div className="text-xs text-red-500 text-center mt-2">{copied} copied!</div>
      )}
      {/* Disclaimer */}
      <div className="text-xs text-muted-foreground text-center mt-6">This is a draft email.</div>
    </div>
  );
};

export default EmailForm;
