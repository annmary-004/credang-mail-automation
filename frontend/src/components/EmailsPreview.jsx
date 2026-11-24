import { useEffect, useState } from 'react'
import toast from 'react-hot-toast'
import API from '../api/auth'
import { RefreshCw, ChevronDown, ChevronUp } from 'lucide-react'

export default function EmailsPreview({ contacts, context, emails, setEmails, generating, setGenerating, onNext, onBack }) {
  const [expanded, setExpanded] = useState(null)
  const [regenIdx, setRegenIdx] = useState(null)

  const generate = async () => {
    setGenerating(true)
    try {
      const { data } = await API.post('/emails/generate', {
        context,
        rows: contacts.rows,
        email_col: contacts.email_col,
      })
      setEmails(data.emails)
      toast.success('Emails generated!')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Generation failed')
    } finally {
      setGenerating(false)
    }
  }

  useEffect(() => { if (emails.length === 0) generate() }, [])

  const regenerate = async (idx) => {
    setRegenIdx(idx)
    try {
      const { data } = await API.post('/emails/regenerate', {
        context,
        row: contacts.rows[idx],
      })
      const updated = [...emails]
      updated[idx] = { ...updated[idx], subject: data.subject, body: data.body }
      setEmails(updated)
      toast.success('Regenerated!')
    } catch {
      toast.error('Regeneration failed')
    } finally {
      setRegenIdx(null)
    }
  }

  const updateField = (idx, field, value) => {
    const updated = [...emails]
    updated[idx] = { ...updated[idx], [field]: value }
    setEmails(updated)
  }

  const validEmails = emails.filter(e => !e.skipped)

  return (
    <div className="max-w-4xl mx-auto space-y-4">
      <div className="card">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h2 className="text-lg font-semibold">Email Preview</h2>
            <p className="text-sm text-gray-500 mt-0.5">
              {validEmails.length} emails ready · {emails.length - validEmails.length} skipped (no email)
            </p>
          </div>
          <div className="flex gap-2">
            <button className="btn-secondary text-sm" onClick={generate} disabled={generating}>
              <RefreshCw className={`w-4 h-4 ${generating ? 'animate-spin' : ''}`} />
              Regenerate All
            </button>
          </div>
        </div>
      </div>

      {generating ? (
        <div className="card text-center py-12 text-blue-600 animate-pulse">
          Generating personalised emails with AI…
        </div>
      ) : (
        <div className="space-y-3">
          {emails.map((email, i) => (
            <div key={i} className={`card border ${email.skipped ? 'border-amber-200 bg-amber-50' : 'border-gray-100'}`}>
              <div className="flex items-start gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-medium text-gray-900">{email.Name || email.name || `Row ${i+1}`}</span>
                    <span className="text-gray-400 text-sm">{email[contacts.email_col]}</span>
                    {email.skipped && (
                      <span className="text-xs bg-amber-100 text-amber-700 px-2 py-0.5 rounded-full">Skipped – no email</span>
                    )}
                  </div>
                  {!email.skipped && (
                    <p className="text-sm text-gray-600 mt-0.5 truncate">
                      <span className="font-medium">Subject:</span> {email.subject}
                    </p>
                  )}
                </div>
                {!email.skipped && (
                  <div className="flex gap-1 shrink-0">
                    <button
                      className="btn-secondary text-xs py-1 px-2"
                      onClick={() => regenerate(i)}
                      disabled={regenIdx === i}
                    >
                      <RefreshCw className={`w-3 h-3 ${regenIdx === i ? 'animate-spin' : ''}`} />
                    </button>
                    <button
                      className="btn-secondary text-xs py-1 px-2"
                      onClick={() => setExpanded(expanded === i ? null : i)}
                    >
                      {expanded === i ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                    </button>
                  </div>
                )}
              </div>

              {expanded === i && !email.skipped && (
                <div className="mt-4 space-y-3 border-t border-gray-100 pt-4">
                  <div>
                    <label className="label text-xs">Subject</label>
                    <input
                      className="input text-sm"
                      value={email.subject}
                      onChange={(e) => updateField(i, 'subject', e.target.value)}
                    />
                  </div>
                  <div>
                    <label className="label text-xs">Body</label>
                    <textarea
                      className="input text-sm min-h-[140px] resize-y"
                      value={email.body}
                      onChange={(e) => updateField(i, 'body', e.target.value)}
                    />
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="flex gap-3 justify-between pt-2">
        <button className="btn-secondary" onClick={onBack}>← Back</button>
        <button className="btn-primary" onClick={onNext} disabled={validEmails.length === 0 || generating}>
          Send {validEmails.length} Email{validEmails.length !== 1 ? 's' : ''} →
        </button>
      </div>
    </div>
  )
}

