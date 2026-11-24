import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import toast from 'react-hot-toast'
import API from '../api/auth'
import { Upload, FileSpreadsheet, AlertCircle } from 'lucide-react'

export default function UploadStep({ onUploaded }) {
  const [loading, setLoading] = useState(false)
  const [preview, setPreview] = useState(null)
  const [emailCol, setEmailCol] = useState('')

  const onDrop = useCallback(async (files) => {
    const file = files[0]
    if (!file) return
    setLoading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      const { data } = await API.post('/contacts/upload', fd)
      setPreview(data)
      setEmailCol(data.email_col || '')
      if (!data.email_col) toast('No email column detected – please select one below', { icon: '⚠️' })
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Upload failed')
    } finally {
      setLoading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
              'application/vnd.ms-excel': ['.xls'], 'text/csv': ['.csv'] },
    multiple: false,
  })

  const proceed = () => {
    if (!emailCol) { toast.error('Please select the Email column first'); return }
    const finalData = {
      ...preview,
      email_col: emailCol,
      rows: preview.rows.map(r => ({ ...r })),
    }
    onUploaded(finalData)
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div className="card">
        <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
          <FileSpreadsheet className="w-5 h-5 text-blue-600" /> Upload Contacts
        </h2>

        <div
          {...getRootProps()}
          className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors ${
            isDragActive ? 'border-blue-400 bg-blue-50' : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
          }`}
        >
          <input {...getInputProps()} />
          <Upload className="w-10 h-10 text-gray-400 mx-auto mb-3" />
          <p className="font-medium text-gray-700">
            {isDragActive ? 'Drop the file here…' : 'Drag & drop an Excel or CSV file'}
          </p>
          <p className="text-sm text-gray-400 mt-1">or click to browse — .xlsx, .xls, .csv</p>
        </div>

        {loading && (
          <div className="mt-4 text-center text-sm text-blue-600 animate-pulse">Processing file…</div>
        )}
      </div>

      {preview && (
        <div className="card space-y-4">
          <div className="flex items-center justify-between flex-wrap gap-3">
            <div>
              <p className="font-semibold text-gray-900">{preview.total} contacts loaded</p>
              {preview.issues_count > 0 && (
                <p className="text-sm text-amber-600 flex items-center gap-1 mt-0.5">
                  <AlertCircle className="w-4 h-4" />
                  {preview.issues_count} row(s) have issues (missing/invalid/duplicate email)
                </p>
              )}
            </div>
            <div className="flex items-center gap-2">
              <label className="label mb-0 whitespace-nowrap">Email column:</label>
              <select
                className="input w-auto"
                value={emailCol}
                onChange={(e) => setEmailCol(e.target.value)}
              >
                <option value="">-- select --</option>
                {preview.columns.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
          </div>

          {/* Preview table */}
          <div className="overflow-auto max-h-72 rounded-lg border border-gray-200">
            <table className="min-w-full text-sm">
              <thead className="bg-gray-50 sticky top-0">
                <tr>
                  {preview.columns.map(c => (
                    <th key={c} className="px-3 py-2 text-left font-medium text-gray-600 border-b border-gray-200">{c}</th>
                  ))}
                  <th className="px-3 py-2 text-left font-medium text-gray-600 border-b border-gray-200">Issues</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100">
                {preview.rows.map((row, i) => (
                  <tr key={i} className={row._issues?.length ? 'bg-amber-50' : ''}>
                    {preview.columns.map(c => (
                      <td key={c} className="px-3 py-1.5 text-gray-700 max-w-xs truncate">{String(row[c] ?? '')}</td>
                    ))}
                    <td className="px-3 py-1.5">
                      {row._issues?.length > 0 && (
                        <span className="text-xs text-amber-700 bg-amber-100 px-2 py-0.5 rounded-full">
                          {row._issues.join(', ')}
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="flex justify-end">
            <button className="btn-primary" onClick={proceed}>
              Continue →
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

