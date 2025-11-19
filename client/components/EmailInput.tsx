import { Textarea } from "@/components/ui/textarea";

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export function EmailInput({ value, onChange }: Props) {
  return (
    <div className="space-y-2">
      <label className="font-medium text-gray-300">Email Text</label>
      <Textarea
        placeholder="Paste or type the email you want analyzed..."
        className="min-h-[200px] bg-neutral-800 border-neutral-700 text-gray-200 placeholder:text-gray-500 focus-visible:ring-orange-500"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
