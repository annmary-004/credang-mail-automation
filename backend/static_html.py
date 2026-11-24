INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Credang – AI Mail Automation</title>
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- SheetJS for local Excel/CSV reading -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    .hidden-step { display: none !important; }
  </style>
</head>
<body class="bg-slate-50 text-slate-800 antialiased min-h-screen flex flex-col">

  <!-- Top Navigation -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 bg-blue-600 rounded-xl flex items-center justify-center shadow-md shadow-blue-500/20 text-white font-bold text-lg">
          C
        </div>
        <div>
          <span class="font-bold text-slate-900 tracking-tight text-lg">Credang</span>
          <span class="ml-2 text-xs font-semibold uppercase tracking-wider bg-blue-50 text-blue-700 px-2 py-0.5 rounded-full border border-blue-200">AI Mail Automation</span>
        </div>
      </div>

      <!-- Auth state header -->
      <div id="authHeader" class="hidden items-center gap-3">
        <div class="flex items-center gap-2 px-3 py-1.5 bg-slate-100 rounded-full text-xs font-medium text-slate-700">
          <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span id="userDisplayName">User</span>
        </div>
        <button onclick="logout()" class="text-xs font-semibold text-slate-600 hover:text-red-600 px-3 py-1.5 rounded-lg border border-slate-200 hover:border-red-200 transition">
          Sign out
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 py-8">

    <!-- ============================================================== -->
    <!-- SCREEN 1: LOGIN / SIGNUP -->
    <!-- ============================================================== -->
    <div id="authSection" class="max-w-md mx-auto my-12">
      <div class="bg-white rounded-2xl border border-slate-200 shadow-xl shadow-slate-100 p-8">
        <div class="text-center mb-6">
          <h1 id="authTitle" class="text-2xl font-bold text-slate-900">Welcome back</h1>
          <p id="authSubtitle" class="text-sm text-slate-500 mt-1">Sign in to start sending personalised AI emails</p>
        </div>

        <form id="authForm" onsubmit="handleAuthSubmit(event)" class="space-y-4">
          <div id="nameFieldGroup" class="hidden">
            <label class="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
            <input id="authName" type="text" placeholder="e.g. Manoj Rajendran"
              class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition">
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Email address</label>
            <input id="authEmail" required type="email" placeholder="you@company.com"
              class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition">
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 mb-1">Password</label>
            <input id="authPassword" required type="password" placeholder="••••••••"
              class="w-full px-3.5 py-2.5 text-sm rounded-xl border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:outline-none transition">
          </div>

          <div id="authErrorBox" class="hidden p-3 bg-red-50 text-red-700 text-xs rounded-xl border border-red-200">
          </div>

          <button id="authSubmitBtn" type="submit"
            class="w-full py-2.5 px-4 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm rounded-xl shadow-lg shadow-blue-500/25 transition">
            Sign in
          </button>
        </form>

        <div class="relative my-6 text-center">
          <div class="absolute inset-0 flex items-center"><div class="w-full border-t border-slate-200"></div></div>
          <span class="relative px-3 bg-white text-xs text-slate-400 uppercase font-medium">Or</span>
        </div>

        <!-- Google Auth Button -->
        <a href="/auth/google"
          class="flex items-center justify-center gap-2.5 w-full py-2.5 px-4 bg-white hover:bg-slate-50 text-slate-700 text-sm font-semibold rounded-xl border border-slate-300 transition">
          <svg class="w-4 h-4" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
          Sign in with Google
        </a>

        <!-- Quick Demo Access -->
        <div class="mt-4 pt-4 border-t border-slate-100 text-center">
          <button onclick="quickDemoLogin()" class="text-xs text-blue-600 hover:text-blue-800 font-semibold underline">
            🚀 Instant Demo Access (Click to bypass login)
          </button>
        </div>

        <div class="mt-5 text-center text-xs text-slate-500">
          <span id="toggleAuthText">Don't have an account? <button onclick="toggleAuthMode()" class="text-blue-600 font-semibold hover:underline">Sign up</button></span>
        </div>
      </div>
    </div>

    <!-- ============================================================== -->
    <!-- SCREEN 2+: AUTHENTICATED WORKFLOW -->
    <!-- ============================================================== -->
    <div id="workflowSection" class="hidden space-y-8">

      <!-- Stepper Progress Bar -->
      <div class="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm">
        <div class="grid grid-cols-4 gap-2 text-center text-xs font-semibold">
          <div id="stepTab1" class="py-2 px-3 rounded-xl bg-blue-600 text-white shadow-md shadow-blue-500/20">
            1. Upload Contacts
          </div>
          <div id="stepTab2" class="py-2 px-3 rounded-xl text-slate-400 bg-slate-50">
            2. Campaign Context
          </div>
          <div id="stepTab3" class="py-2 px-3 rounded-xl text-slate-400 bg-slate-50">
            3. AI Review & Edit
          </div>
          <div id="stepTab4" class="py-2 px-3 rounded-xl text-slate-400 bg-slate-50">
            4. Live Delivery & Report
          </div>
        </div>
      </div>

      <!-- ──────────────── STEP 1: UPLOAD & PREVIEW ──────────────── -->
      <div id="step1Content" class="space-y-6">
        <div class="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
          <div class="max-w-xl mx-auto text-center">
            <div class="w-14 h-14 bg-blue-50 text-blue-600 rounded-2xl mx-auto flex items-center justify-center mb-4">
              <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path></svg>
            </div>
            <h2 class="text-xl font-bold text-slate-900">Upload Contact List</h2>
            <p class="text-sm text-slate-500 mt-1">Upload an Excel (.xlsx, .xls) or CSV file with your contact leads.</p>

            <!-- Drag and drop box -->
            <div id="dropZone" onclick="document.getElementById('fileInput').click()"
              class="mt-6 border-2 border-dashed border-slate-300 hover:border-blue-400 hover:bg-slate-50 rounded-2xl p-8 cursor-pointer transition">
              <input id="fileInput" type="file" accept=".xlsx,.xls,.csv" class="hidden" onchange="handleFileSelected(event)">
              <p class="text-sm font-semibold text-slate-700">Click to browse or drag & drop file here</p>
              <p class="text-xs text-slate-400 mt-1">Supports contacts.xlsx, .xls, .csv</p>
            </div>

            <!-- Quick sample load -->
            <div class="mt-4 flex items-center justify-center gap-2">
              <span class="text-xs text-slate-400">or test with</span>
              <button onclick="loadSampleData()" class="text-xs font-semibold text-blue-600 hover:text-blue-800 underline">
                Sample contacts.xlsx (Manoj Rajendran & team)
              </button>
            </div>
          </div>
        </div>

        <!-- Contacts Preview Table -->
        <div id="previewTableCard" class="hidden bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 class="font-bold text-slate-900">Contact Preview & Validation</h3>
              <p id="tableSummaryText" class="text-xs text-slate-500">Loaded contacts</p>
            </div>

            <!-- Column selector -->
            <div class="flex items-center gap-2">
              <label class="text-xs font-semibold text-slate-600">Email Column:</label>
              <select id="emailColSelect" onchange="changeEmailColumn(event)" class="text-xs font-medium bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1.5 focus:ring-2 focus:ring-blue-500 focus:outline-none">
              </select>
            </div>
          </div>

          <!-- Table Container -->
          <div class="overflow-x-auto border border-slate-200 rounded-xl">
            <table class="w-full text-left text-xs">
              <thead id="previewTableHead" class="bg-slate-50 border-b border-slate-200 text-slate-600 uppercase font-semibold">
              </thead>
              <tbody id="previewTableBody" class="divide-y divide-slate-100">
              </tbody>
            </table>
          </div>

          <div class="flex justify-end pt-2">
            <button id="step1ContinueBtn" onclick="goToStep(2)"
              class="py-2.5 px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm rounded-xl shadow-md shadow-blue-500/20 transition">
              Continue to Campaign Context →
            </button>
          </div>
        </div>
      </div>

      <!-- ──────────────── STEP 2: CAMPAIGN CONTEXT ──────────────── -->
      <div id="step2Content" class="hidden max-w-2xl mx-auto space-y-6">
        <div class="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm space-y-6">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Campaign Instructions & Context</h2>
            <p class="text-sm text-slate-500 mt-1">
              Tell the LLM the purpose of this email. Use <code class="bg-slate-100 text-blue-600 px-1.5 py-0.5 rounded text-xs font-mono font-semibold">{{Name}}</code> to personalise greetings.
            </p>
          </div>

          <div class="space-y-4">
            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Purpose & Pitch</label>
              <textarea id="campaignPurpose" rows="4" placeholder="e.g. Inviting AI & ML engineers to explore the Credang automated outreach platform and schedule a quick 10-minute partnership demo."
                class="w-full text-sm rounded-xl border border-slate-300 p-3 focus:ring-2 focus:ring-blue-500 focus:outline-none transition">Inviting AI & ML engineers to test the Credang automated email outreach platform and see a 5-minute live preview.</textarea>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Tone of Voice</label>
                <select id="campaignTone" class="w-full text-sm rounded-xl border border-slate-300 px-3 py-2.5 focus:ring-2 focus:ring-blue-500 focus:outline-none">
                  <option value="Professional yet warm">Professional & Warm</option>
                  <option value="Casual and friendly">Casual & Friendly</option>
                  <option value="Direct and concise">Direct & Concise</option>
                  <option value="Executive and formal">Executive & Formal</option>
                </select>
              </div>

              <div>
                <label class="block text-xs font-semibold text-slate-700 mb-1">Sender Signature</label>
                <input id="campaignSender" type="text" value="Manoj Rajendran, Head of Data Solutions, Credang"
                  class="w-full text-sm rounded-xl border border-slate-300 px-3 py-2.5 focus:ring-2 focus:ring-blue-500 focus:outline-none">
              </div>
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 mb-1">Call to Action (CTA)</label>
              <input id="campaignCta" type="text" value="Could we connect for a quick 10-minute discovery call this Thursday?"
                class="w-full text-sm rounded-xl border border-slate-300 px-3 py-2.5 focus:ring-2 focus:ring-blue-500 focus:outline-none">
            </div>
          </div>

          <div class="flex items-center justify-between pt-4 border-t border-slate-100">
            <button onclick="goToStep(1)" class="text-sm font-semibold text-slate-600 hover:text-slate-800">
              ← Back
            </button>
            <button id="generateBtn" onclick="generateEmails()"
              class="py-2.5 px-6 bg-blue-600 hover:bg-blue-700 text-white font-semibold text-sm rounded-xl shadow-md shadow-blue-500/20 transition flex items-center gap-2">
              <span>Generate AI Emails →</span>
            </button>
          </div>
        </div>
      </div>

      <!-- ──────────────── STEP 3: REVIEW & EDIT ──────────────── -->
      <div id="step3Content" class="hidden space-y-6">
        <div class="flex items-center justify-between">
          <div>
            <h2 class="text-xl font-bold text-slate-900">Personalised Emails Review</h2>
            <p class="text-sm text-slate-500">Review, modify, or regenerate any message before sending.</p>
          </div>
          <button onclick="generateEmails()" class="text-xs font-semibold text-blue-600 hover:text-blue-800 border border-blue-200 hover:border-blue-300 bg-white px-3 py-2 rounded-xl transition">
            🔄 Regenerate All
          </button>
        </div>

        <div id="emailsListContainer" class="grid grid-cols-1 gap-6">
        </div>

        <div class="flex items-center justify-between pt-4">
          <button onclick="goToStep(2)" class="text-sm font-semibold text-slate-600 hover:text-slate-800">
            ← Back to Context
          </button>
          <button id="sendEmailsBtn" onclick="sendAllEmails()"
            class="py-3 px-8 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold text-sm rounded-xl shadow-lg shadow-emerald-500/25 transition flex items-center gap-2">
            <span>Send Personalised Emails 🚀</span>
          </button>
        </div>
      </div>

      <!-- ──────────────── STEP 4: SEND STATUS & REPORT ──────────────── -->
      <div id="step4Content" class="hidden space-y-6">
        <div class="bg-white rounded-2xl border border-slate-200 p-8 shadow-sm">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-6">
            <div>
              <h2 class="text-xl font-bold text-slate-900">Email Dispatch Dashboard</h2>
              <p class="text-xs text-slate-500 mt-1">Real-time delivery monitor with retry and CSV audit logs.</p>
            </div>

            <div class="flex items-center gap-3">
              <a href="/emails/report" download="email_report.csv"
                class="py-2.5 px-4 bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs rounded-xl shadow transition flex items-center gap-2">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                Download CSV Report
              </a>
              <button onclick="restartWorkflow()" class="py-2.5 px-4 bg-blue-50 text-blue-700 hover:bg-blue-100 font-semibold text-xs rounded-xl transition">
                + New Campaign
              </button>
            </div>
          </div>

          <!-- Stats Bar -->
          <div class="grid grid-cols-3 gap-4 my-6">
            <div class="bg-blue-50/60 border border-blue-100 p-4 rounded-xl">
              <div class="text-xs font-semibold text-blue-600 uppercase">Queued</div>
              <div id="statQueued" class="text-2xl font-bold text-blue-900 mt-1">0</div>
            </div>
            <div class="bg-emerald-50/60 border border-emerald-100 p-4 rounded-xl">
              <div class="text-xs font-semibold text-emerald-600 uppercase">Delivered</div>
              <div id="statSent" class="text-2xl font-bold text-emerald-900 mt-1">0</div>
            </div>
            <div class="bg-rose-50/60 border border-rose-100 p-4 rounded-xl">
              <div class="text-xs font-semibold text-rose-600 uppercase">Failed</div>
              <div id="statFailed" class="text-2xl font-bold text-rose-900 mt-1">0</div>
            </div>
          </div>

          <!-- Live Table -->
          <div class="overflow-x-auto border border-slate-200 rounded-xl">
            <table class="w-full text-left text-xs">
              <thead class="bg-slate-50 border-b border-slate-200 text-slate-600 uppercase font-semibold">
                <tr>
                  <th class="py-3 px-4">Recipient</th>
                  <th class="py-3 px-4">Subject</th>
                  <th class="py-3 px-4">Status</th>
                  <th class="py-3 px-4">Timestamp / Details</th>
                </tr>
              </thead>
              <tbody id="logsTableBody" class="divide-y divide-slate-100">
              </tbody>
            </table>
          </div>

        </div>
      </div>

    </div>
  </main>

  <!-- Footer -->
  <footer class="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-400">
    Credang AI Mail Automation · Full-Stack Evaluation Build
  </footer>

  <!-- Vanilla JavaScript Logic (Zero External Frameworks - 100% Reliable) -->
  <script>
    // Global Application State
    let currentUser = null;
    let authToken = localStorage.getItem('token') || '';
    let isRegisterMode = false;
    let currentStep = 1;
    let rawContacts = [];
    let tableColumns = [];
    let selectedEmailColumn = '';
    let generatedEmailsList = [];
    let statusPollInterval = null;

    // Initialization
    window.addEventListener('DOMContentLoaded', () => {
      // Check query params for Google OAuth redirect
      const params = new URLSearchParams(window.location.search);
      const token = params.get('token');
      if (token) {
        authToken = token;
        localStorage.setItem('token', token);
        const name = params.get('name') || '';
        const email = params.get('email') || '';
        currentUser = { name, email };
        window.history.replaceState({}, document.title, window.location.pathname);
      }

      if (authToken) {
        verifyAuth();
      } else {
        showAuthScreen();
      }

      // Drag & drop listeners
      const dropZone = document.getElementById('dropZone');
      if (dropZone) {
        dropZone.addEventListener('dragover', (e) => { e.preventDefault(); dropZone.classList.add('border-blue-500', 'bg-blue-50'); });
        dropZone.addEventListener('dragleave', (e) => { e.preventDefault(); dropZone.classList.remove('border-blue-500', 'bg-blue-50'); });
        dropZone.addEventListener('drop', (e) => {
          e.preventDefault();
          dropZone.classList.remove('border-blue-500', 'bg-blue-50');
          if (e.dataTransfer.files.length) parseUploadedFile(e.dataTransfer.files[0]);
        });
      }
    });

    async function verifyAuth() {
      try {
        const res = await fetch('/auth/me', { headers: { 'Authorization': `Bearer ${authToken}` } });
        if (res.ok) {
          currentUser = await res.json();
          showWorkflowScreen();
        } else {
          logout();
        }
      } catch (e) {
        logout();
      }
    }

    function showAuthScreen() {
      document.getElementById('authHeader').classList.add('hidden');
      document.getElementById('authHeader').classList.remove('flex');
      document.getElementById('authSection').classList.remove('hidden');
      document.getElementById('workflowSection').classList.add('hidden');
    }

    function showWorkflowScreen() {
      document.getElementById('authHeader').classList.remove('hidden');
      document.getElementById('authHeader').classList.add('flex');
      document.getElementById('userDisplayName').textContent = currentUser.name || currentUser.email;
      document.getElementById('authSection').classList.add('hidden');
      document.getElementById('workflowSection').classList.remove('hidden');
      goToStep(1);
    }

    function toggleAuthMode() {
      isRegisterMode = !isRegisterMode;
      document.getElementById('authTitle').textContent = isRegisterMode ? 'Create your account' : 'Welcome back';
      document.getElementById('authSubtitle').textContent = isRegisterMode ? 'Sign up to start automating emails' : 'Sign in to start sending personalised AI emails';
      document.getElementById('nameFieldGroup').classList.toggle('hidden', !isRegisterMode);
      document.getElementById('authSubmitBtn').textContent = isRegisterMode ? 'Sign up' : 'Sign in';
      document.getElementById('toggleAuthText').innerHTML = isRegisterMode
        ? 'Already have an account? <button onclick="toggleAuthMode()" class="text-blue-600 font-semibold hover:underline">Sign in</button>'
        : 'Don\'t have an account? <button onclick="toggleAuthMode()" class="text-blue-600 font-semibold hover:underline">Sign up</button>';
      document.getElementById('authErrorBox').classList.add('hidden');
    }

    async function handleAuthSubmit(e) {
      e.preventDefault();
      const errorBox = document.getElementById('authErrorBox');
      errorBox.classList.add('hidden');
      const submitBtn = document.getElementById('authSubmitBtn');
      submitBtn.disabled = true;
      submitBtn.textContent = 'Please wait...';

      const email = document.getElementById('authEmail').value;
      const password = document.getElementById('authPassword').value;
      const name = document.getElementById('authName').value;

      try {
        let res;
        if (isRegisterMode) {
          res = await fetch('/auth/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password, name })
          });
        } else {
          const fd = new URLSearchParams();
          fd.append('username', email);
          fd.append('password', password);
          res = await fetch('/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: fd
          });
        }

        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Authentication failed');

        authToken = data.access_token;
        localStorage.setItem('token', authToken);
        currentUser = { name: data.name, email: data.email };
        showWorkflowScreen();
      } catch (err) {
        errorBox.textContent = err.message;
        errorBox.classList.remove('hidden');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = isRegisterMode ? 'Sign up' : 'Sign in';
      }
    }

    async function quickDemoLogin() {
      document.getElementById('authEmail').value = 'evaluator@credang.com';
      document.getElementById('authPassword').value = 'Credang2026!';
      document.getElementById('authName').value = 'Manoj Rajendran';
      isRegisterMode = true;
      await handleAuthSubmit(new Event('submit'));
      if (document.getElementById('authErrorBox').classList.contains('hidden') === false) {
        isRegisterMode = false;
        await handleAuthSubmit(new Event('submit'));
      }
    }

    function logout() {
      currentUser = null;
      authToken = '';
      localStorage.removeItem('token');
      showAuthScreen();
    }

    // Step Navigation
    function goToStep(step) {
      currentStep = step;
      [1, 2, 3, 4].forEach(s => {
        document.getElementById(`step${s}Content`).classList.toggle('hidden', s !== step);
        const tab = document.getElementById(`stepTab${s}`);
        if (s === step) {
          tab.className = 'py-2 px-3 rounded-xl bg-blue-600 text-white shadow-md shadow-blue-500/20';
        } else if (s < step) {
          tab.className = 'py-2 px-3 rounded-xl bg-emerald-50 text-emerald-700 border border-emerald-200';
        } else {
          tab.className = 'py-2 px-3 rounded-xl text-slate-400 bg-slate-50';
        }
      });
    }

    // File Upload & Preview Table
    function handleFileSelected(e) {
      if (e.target.files.length) parseUploadedFile(e.target.files[0]);
    }

    function loadSampleData() {
      const sample = [
        { "Name": "Manoj Rajendran", "Email": "manoj_rajendran@credang.com", "Company": "Credang", "Role": "Head of Data Solutions" },
        { "Name": "Alex Morgan", "Email": "alex.m@apexai.io", "Company": "Apex Labs", "Role": "AI Specialist" },
        { "Name": "Sara Chen", "Email": "sara.chen@enterprise.io", "Company": "Enterprise AI", "Role": "Director of Engineering" }
      ];
      tableColumns = ["Name", "Email", "Company", "Role"];
      selectedEmailColumn = "Email";
      renderPreview(sample);
    }

    function parseUploadedFile(file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = new Uint8Array(e.target.result);
          const workbook = XLSX.read(data, { type: 'array' });
          const firstSheet = workbook.SheetNames[0];
          const json = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheet]);
          if (!json.length) return alert('The uploaded file contains no data.');

          tableColumns = Object.keys(json[0]);
          selectedEmailColumn = tableColumns.find(c => c.toLowerCase().includes('email') || c.toLowerCase().includes('mail')) || tableColumns[0];
          renderPreview(json);
        } catch (err) {
          alert('Failed to parse file: ' + err.message);
        }
      };
      reader.readAsArrayBuffer(file);
    }

    function renderPreview(rows) {
      const seen = new Set();
      rawContacts = rows.map(r => {
        const val = (r[selectedEmailColumn] || '').toString().trim();
        let err = null;
        if (!val) err = 'Missing Email';
        else if (!val.includes('@') || !val.includes('.')) err = 'Invalid Email';
        else if (seen.has(val.toLowerCase())) err = 'Duplicate Email';
        else seen.add(val.toLowerCase());
        return { ...r, _error: err };
      });

      // Update Column dropdown
      const select = document.getElementById('emailColSelect');
      select.innerHTML = tableColumns.map(c => `<option value="${c}" ${c === selectedEmailColumn ? 'selected' : ''}>${c}</option>`).join('');

      // Header
      const head = document.getElementById('previewTableHead');
      head.innerHTML = `<tr><th class="py-3 px-4">#</th>${tableColumns.map(c => `<th class="py-3 px-4">${c}</th>`).join('')}<th class="py-3 px-4">Status</th></tr>`;

      // Body
      const body = document.getElementById('previewTableBody');
      body.innerHTML = rawContacts.map((r, i) => `
        <tr class="${r._error ? 'bg-amber-50/60' : 'hover:bg-slate-50'}">
          <td class="py-3 px-4 text-slate-400 font-mono">${i + 1}</td>
          ${tableColumns.map(c => `<td class="py-3 px-4 font-medium text-slate-800">${r[c] || '-'}</td>`).join('')}
          <td class="py-3 px-4">
            <span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold ${r._error ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'}">
              ${r._error || 'Valid'}
            </span>
          </td>
        </tr>
      `).join('');

      const validCount = rawContacts.filter(c => !c._error).length;
      document.getElementById('tableSummaryText').textContent = `Found ${rawContacts.length} rows (${validCount} valid leads ready).`;
      document.getElementById('step1ContinueBtn').textContent = `Continue with ${validCount} valid lead(s) →`;
      document.getElementById('previewTableCard').classList.remove('hidden');
    }

    function changeEmailColumn(e) {
      selectedEmailColumn = e.target.value;
      renderPreview(rawContacts);
    }

    // Step 3: LLM Generation
    async function generateEmails() {
      const btn = document.getElementById('generateBtn');
      btn.disabled = true;
      btn.innerHTML = `<span class="animate-spin">⏳</span> Generating Personalised Emails...`;

      const purpose = document.getElementById('campaignPurpose').value;
      const tone = document.getElementById('campaignTone').value;
      const sender = document.getElementById('campaignSender').value;
      const cta = document.getElementById('campaignCta').value;
      const contextText = `Purpose: ${purpose}\nTone: ${tone}\nSender/Signature: ${sender}\nCall-to-Action: ${cta}`;

      const validRows = rawContacts.filter(c => !c._error);

      try {
        const res = await fetch('/emails/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${authToken}`
          },
          body: JSON.stringify({
            context: contextText,
            rows: validRows,
            email_col: selectedEmailColumn
          })
        });

        if (!res.ok) throw new Error('Generation failed');
        const data = await res.json();
        generatedEmailsList = data.emails.map(e => ({
          ...e,
          recipient_name: e.Name || e.name || 'Recipient',
          recipient_email: e[selectedEmailColumn] || e.email
        }));

        renderGeneratedEmails();
        goToStep(3);
      } catch (err) {
        alert('Error: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<span>Generate AI Emails →</span>`;
      }
    }

    function renderGeneratedEmails() {
      const container = document.getElementById('emailsListContainer');
      container.innerHTML = generatedEmailsList.map((item, idx) => `
        <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm space-y-4">
          <div class="flex items-center justify-between border-b border-slate-100 pb-3">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-xs">
                ${(item.recipient_name || 'U').charAt(0)}
              </div>
              <div>
                <h4 class="font-bold text-sm text-slate-900">${item.recipient_name}</h4>
                <p class="text-xs text-slate-400 font-mono">${item.recipient_email}</p>
              </div>
            </div>
            <button onclick="regenerateEmailSingle(${idx})" id="regenBtn_${idx}" class="text-xs text-slate-600 hover:text-blue-600 font-medium px-2.5 py-1 rounded-lg border border-slate-200 hover:border-blue-300 transition">
              🔄 Regenerate
            </button>
          </div>
          <div class="space-y-3">
            <div>
              <label class="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Subject</label>
              <input type="text" value="${item.subject.replace(/"/g, '&quot;')}" onchange="updateEmailField(${idx}, 'subject', this.value)"
                class="w-full text-sm font-medium text-slate-800 rounded-xl border border-slate-200 px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none">
            </div>
            <div>
              <label class="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1">Body</label>
              <textarea rows="6" onchange="updateEmailField(${idx}, 'body', this.value)"
                class="w-full text-xs font-normal text-slate-700 rounded-xl border border-slate-200 p-3 focus:ring-2 focus:ring-blue-500 focus:outline-none leading-relaxed">${item.body}</textarea>
            </div>
          </div>
        </div>
      `).join('');

      document.getElementById('sendEmailsBtn').innerHTML = `<span>Send ${generatedEmailsList.length} Personalised Emails 🚀</span>`;
    }

    function updateEmailField(idx, field, value) {
      generatedEmailsList[idx][field] = value;
    }

    async function regenerateEmailSingle(idx) {
      const btn = document.getElementById(`regenBtn_${idx}`);
      btn.textContent = '⏳ Thinking...';
      const item = generatedEmailsList[idx];

      const purpose = document.getElementById('campaignPurpose').value;
      const tone = document.getElementById('campaignTone').value;
      const sender = document.getElementById('campaignSender').value;
      const cta = document.getElementById('campaignCta').value;
      const contextText = `Purpose: ${purpose}\nTone: ${tone}\nSender/Signature: ${sender}\nCall-to-Action: ${cta}`;

      try {
        const res = await fetch('/emails/regenerate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authToken}` },
          body: JSON.stringify({ context: contextText, row: item })
        });
        const data = await res.json();
        item.subject = data.subject;
        item.body = data.body;
        renderGeneratedEmails();
      } catch (e) {
        alert('Regeneration error: ' + e.message);
      } finally {
        btn.textContent = '🔄 Regenerate';
      }
    }

    // Step 4: Dispatch
    async function sendAllEmails() {
      const btn = document.getElementById('sendEmailsBtn');
      btn.disabled = true;
      btn.innerHTML = `<span>Dispatching...</span>`;

      try {
        const payload = {
          logs: generatedEmailsList.map(e => ({
            log_id: e.log_id,
            recipient_email: e.recipient_email,
            subject: e.subject,
            body: e.body
          }))
        };

        const res = await fetch('/emails/send', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authToken}` },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.detail || 'Send failed');
        }

        goToStep(4);
        startPolling();
      } catch (err) {
        alert('Send failed: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.innerHTML = `<span>Send ${generatedEmailsList.length} Personalised Emails 🚀</span>`;
      }
    }

    function startPolling() {
      if (statusPollInterval) clearInterval(statusPollInterval);
      const poll = async () => {
        try {
          const res = await fetch('/emails/status', { headers: { 'Authorization': `Bearer ${authToken}` } });
          if (res.ok) {
            const data = await res.json();
            renderLiveLogs(data.logs);
          }
        } catch (e) {}
      };
      poll();
      statusPollInterval = setInterval(poll, 2000);
    }

    function renderLiveLogs(logs) {
      let q = 0, s = 0, f = 0;
      logs.forEach(l => {
        if (l.status === 'sent') s++;
        else if (l.status === 'failed') f++;
        else q++;
      });
      document.getElementById('statQueued').textContent = q;
      document.getElementById('statSent').textContent = s;
      document.getElementById('statFailed').textContent = f;

      const body = document.getElementById('logsTableBody');
      body.innerHTML = logs.map(l => `
        <tr class="hover:bg-slate-50">
          <td class="py-3 px-4 font-semibold text-slate-800">
            ${l.recipient_name}
            <span class="block text-[11px] font-normal text-slate-400 font-mono">${l.recipient_email}</span>
          </td>
          <td class="py-3 px-4 text-slate-600 font-medium max-w-xs truncate">${l.subject}</td>
          <td class="py-3 px-4">
            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider ${
              l.status === 'sent' ? 'bg-emerald-100 text-emerald-800' :
              l.status === 'failed' ? 'bg-rose-100 text-rose-800' :
              'bg-amber-100 text-amber-800'
            }">
              ${l.status}
            </span>
          </td>
          <td class="py-3 px-4 text-slate-500 font-mono text-[11px]">
            ${l.error_msg || l.sent_at || l.created_at || 'In progress...'}
          </td>
        </tr>
      `).join('');
    }

    function restartWorkflow() {
      if (statusPollInterval) clearInterval(statusPollInterval);
      goToStep(1);
    }
  </script>
</body>
</html>
"""
