import { useState, useEffect } from 'react'
import toast from 'react-hot-toast'
import API from '../api/auth'
import { Send, CheckCircle, XCircle, Clock, RefreshCw } from 'lucide-react'

const STATUS_ICON = {
  queued: <Clock className="w-4 h-4 text-gray-400" />,
  sent:   <CheckCircle className="w-4 h-4 text-green-500" />,
  failed: <XCircle className="w-4 h-4 text-red-500" />,
}

export default function SendStatus({ emails, onDone, onBack }) {
  const [sending, setSending] = useState(false)
  const [logs, setLogs]       = useState([])
  const [polling, setPolling] = useState(false)
  const [sent, setSent]       = useState(false)

  const validEmails = emails.filter(e => !e.skipped && e.log_id)

  const sendAll = async () => {
    setSending(true)
    try {
      await API.post('/emails/send', {
        logs: validEmails.map(e => ({
          log_id: e.log_id,
          recipient_email: e[Object.keys(e).find(k => k.toLowerCase().includes('email'))] || '',
          subject: e.subject,
          body: e.body,
        })),
      })
      toast.success('Sending emails in background…')
      setSent(true)
      setPolling(true)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Send failed')
    } finally {
      setSending(false)
    }
  }

  // Poll status
  useEffect(() => {
    if (!polling) return
    const interval = setInterval(async () => {
      try {
        const { data } = await API.get('/emails/status')
        setLogs(data.logs)
        const allDone = data.logs.every(l => l.status === 'sent' || l.status === 'failed')
        if (allDone && data.logs.length > 0) {
          setPolling(false)
          const failed = data.logs.filter(l => l.status === 'failed').length
          if (failed) toast.error(`${failed} email(s) failed`)
          else toast.success('All emails sent!')
        }
      } catch {}
    }, 3000)
    return () => clearInterval(interval)
  }, [polling])

  return (
    <div className="max-w-3xl mx-auto space-y-5">
      <div className="card">
        <h2 className="text-lg font-semibold mb-1">Send Emails</h2>
        <p className="text-sm text-gray-500">
          {validEmails.length} email{validEmails.length !== 1 ? 's' : ''} will be sent via SMTP in the background.
          Each row shows Queued → Sent / Failed.
        </p>
      </div>

      {!sent ? (
        <div className="card text-center space-y-4">
          <Send className="w-12 h-12 text-blue-500 mx-auto" />
          <p className="text-gray-700 font-medium">Ready to send {validEmails.length} personalised email{validEmails.length !== 1 ? 's' : ''}?</p>
          <div className="flex gap-3 justify-center">
            <button className="btn-secondary" onClick={onBack}>← Back</button>
            <button className="btn-green" onClick={sendAll} disabled={sending}>
              {sending ? 'Sending…' : `Send Now`}
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-semibold text-gray-900">Sending Status</h3>
              {polling && <span className="text-xs text-blue-600 flex items-center gap-1 animate-pulse"><RefreshCw className="w-3 h-3" /> Refreshing…</span>}
            </div>

            <div className="space-y-2 max-h-96 overflow-auto">
              {logs.length === 0 && <p className="text-gray-400 text-sm text-center py-4">Waiting for status…</p>}
              {logs.map(log => (
                <div key={log.id} className="flex items-center gap-3 p-3 rounded-lg border border-gray-100">
                  {STATUS_ICON[log.status] || STATUS_ICON.queued}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{log.recipient_name} &lt;{log.recipient_email}&gt;</p>
                    <p className="text-xs text-gray-500 truncate">{log.subject}</p>
                    {log.error_msg && <p className="text-xs text-red-500 mt-0.5">{log.error_msg}</p>}
                  </div>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${
                    log.status === 'sent'   ? 'bg-green-100 text-green-700' :
                    log.status === 'failed' ? 'bg-red-100 text-red-700' :
                    'bg-gray-100 text-gray-600'
                  }`}>{log.status}</span>
                </div>
              ))}
            </div>
          </div>

          {!polling && logs.length > 0 && (
            <div className="flex justify-end">
              <button className="btn-primary" onClick={onDone}>View Report →</button>
            </div>
          )}
        </>
      )}
    </div>
  )
}

