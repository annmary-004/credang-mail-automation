import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { clearAuth, useAuth } from '../api/auth'
import UploadStep from '../components/UploadStep'
import PreviewTable from '../components/PreviewTable'
import ContextStep from '../components/ContextStep'
import EmailsPreview from '../components/EmailsPreview'
import SendStatus from '../components/SendStatus'
import { LogOut, Mail, Upload, Settings, Send, CheckCircle } from 'lucide-react'

const STEPS = ['Upload', 'Context', 'Generate', 'Send', 'Report']

export default function DashboardPage() {
  const navigate = useNavigate()
  const { name, email } = useAuth()

  const [step,      setStep]      = useState(0)
  const [contacts,  setContacts]  = useState(null)   // { columns, email_col, rows }
  const [context,   setContext]   = useState('')
  const [emails,    setEmails]    = useState([])
  const [generating, setGenerating] = useState(false)

  const logout = () => {
    clearAuth()
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navbar */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-blue-600 rounded-md flex items-center justify-center">
              <span className="text-white font-bold text-xs">C</span>
            </div>
            <span className="font-semibold text-gray-900">Credang AI Mail</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-500 hidden sm:block">{name || email}</span>
            <button onClick={logout} className="btn-secondary text-sm py-1.5">
              <LogOut className="w-4 h-4" /> Logout
            </button>
          </div>
        </div>
      </header>

      {/* Stepper */}
      <div className="bg-white border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-4 py-3">
          <ol className="flex items-center gap-1 overflow-x-auto">
            {STEPS.map((s, i) => (
              <li key={s} className="flex items-center gap-1 shrink-0">
                <button
                  onClick={() => i < step && setStep(i)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-colors ${
                    i === step
                      ? 'bg-blue-100 text-blue-700'
                      : i < step
                      ? 'text-green-700 hover:bg-green-50'
                      : 'text-gray-400 cursor-default'
                  }`}
                >
                  {i < step ? (
                    <CheckCircle className="w-4 h-4 text-green-500" />
                  ) : (
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center text-xs font-bold ${
                      i === step ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-500'
                    }`}>{i + 1}</span>
                  )}
                  {s}
                </button>
                {i < STEPS.length - 1 && <span className="text-gray-300 mx-0.5">›</span>}
              </li>
            ))}
          </ol>
        </div>
      </div>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {step === 0 && (
          <UploadStep
            onUploaded={(data) => { setContacts(data); setStep(1) }}
          />
        )}
        {step === 1 && contacts && (
          <ContextStep
            contacts={contacts}
            context={context}
            onContextChange={setContext}
            onNext={() => setStep(2)}
            onBack={() => setStep(0)}
          />
        )}
        {step === 2 && contacts && (
          <EmailsPreview
            contacts={contacts}
            context={context}
            emails={emails}
            setEmails={setEmails}
            generating={generating}
            setGenerating={setGenerating}
            onNext={() => setStep(3)}
            onBack={() => setStep(1)}
          />
        )}
        {step === 3 && (
          <SendStatus
            emails={emails}
            onDone={() => setStep(4)}
            onBack={() => setStep(2)}
          />
        )}
        {step === 4 && (
          <div className="card text-center max-w-lg mx-auto">
            <CheckCircle className="w-16 h-16 text-green-500 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">All done! 🎉</h2>
            <p className="text-gray-500 mb-6">Your personalised emails have been sent.</p>
            <div className="flex gap-3 justify-center flex-wrap">
              <a href="/api/emails/report" className="btn-primary">
                <Send className="w-4 h-4" /> Download CSV Report
              </a>
              <button onClick={() => { setContacts(null); setEmails([]); setStep(0) }} className="btn-secondary">
                Start New Campaign
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

