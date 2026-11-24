export default function ContextStep({ contacts, context, onContextChange, onNext, onBack }) {
  return (
    <div className="max-w-2xl mx-auto">
      <div className="card space-y-5">
        <h2 className="text-lg font-semibold">Email Context</h2>
        <p className="text-sm text-gray-500">
          Describe the purpose, tone, your name/signature, and desired call-to-action.
          The LLM will use this to personalise each email.
        </p>

        <div>
          <label className="label">Context / Instructions</label>
          <textarea
            className="input min-h-[180px] resize-y"
            placeholder={`Example:\nPurpose: Invite contacts to our AI webinar on Dec 10.\nTone: Friendly and professional.\nSender: Manoj Rajendran, Head of Partnerships, Credang.\nCTA: Register at https://credang.com/webinar\n\nUse {{Name}} to personalise greetings.`}
            value={context}
            onChange={(e) => onContextChange(e.target.value)}
          />
        </div>

        <div className="bg-blue-50 rounded-lg p-3 text-sm text-blue-700">
          <strong>Tip:</strong> Use <code className="bg-blue-100 px-1 rounded">{"{{Name}}"}</code> in your context — it will be replaced with each contact's name automatically.
        </div>

        <div className="flex gap-3 justify-between">
          <button className="btn-secondary" onClick={onBack}>← Back</button>
          <button
            className="btn-primary"
            onClick={onNext}
            disabled={!context.trim()}
          >
            Generate Emails →
          </button>
        </div>
      </div>
    </div>
  )
}

