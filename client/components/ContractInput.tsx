import { Textarea } from "@/components/ui/textarea";

interface Props {
  value: string;
  onChange: (v: string) => void;
}

export function ContractInput({ value, onChange }: Props) {
  return (
    <div className="space-y-2 mt-4">
      <label className="font-medium text-gray-300">Contract Snippet</label>
      <Textarea
        placeholder="Paste relevant contract clauses here..."
        className="min-h-[200px] bg-neutral-800 border-neutral-700 text-gray-200 placeholder:text-gray-500 focus-visible:ring-orange-500"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
