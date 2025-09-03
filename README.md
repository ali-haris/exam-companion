<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Exam Companion – README</title>
  <meta name="description" content="Exam Companion is an AI-driven study planner that generates personalized study schedules for stress-free exam prep." />
  <style>
    :root {
      --bg: #0b0c10;
      --card: #111317;
      --text: #eaf0f6;
      --muted: #a9b2c3;
      --brand: #6ee7b7; /* mint */
      --brand-2: #60a5fa; /* blue */
      --accent: #f59e0b; /* amber */
      --border: #222633;
      --code: #0f172a;
      --shadow: 0 10px 30px rgba(0,0,0,.35);
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; }
    body {
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji";
      color: var(--text);
      background: radial-gradient(1200px 800px at 75% -10%, rgba(96,165,250,.08), transparent 60%),
                  radial-gradient(1000px 700px at 10% 10%, rgba(110,231,183,.06), transparent 55%),
                  var(--bg);
      line-height: 1.65;
    }
    a { color: var(--brand-2); text-decoration: none; }
    a:hover { text-decoration: underline; }

    .wrap { max-width: 1024px; margin: 0 auto; padding: 40px 20px 80px; }

    .hero {
      background: linear-gradient(180deg, rgba(17,19,23,.8), rgba(17,19,23,.6));
      border: 1px solid var(--border);
      border-radius: 20px;
      padding: 36px;
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
      isolation: isolate;
    }
    .hero::after {
      content: ""; position: absolute; inset: -40% -40% auto auto; height: 260px; width: 260px;
      background: radial-gradient(closest-side, rgba(110,231,183,.25), transparent 70%);
      filter: blur(20px); z-index: -1; opacity: .7;
    }
    .title { font-size: clamp(30px, 4vw, 46px); line-height: 1.1; margin: 0 0 8px; }
    .subtitle { margin: 0; color: var(--muted); font-size: 1.05rem; }

    .badges { margin-top: 18px; display: flex; flex-wrap: wrap; gap: 10px; }
    .badges img { height: 22px; }

    .cta { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px; }
    .btn {
      display: inline-flex; align-items: center; gap: 10px; padding: 12px 16px;
      border-radius: 999px; border: 1px solid var(--border);
      background: linear-gradient(180deg, #151821, #10131a);
      color: var(--text); text-decoration: none; font-weight: 600;
      box-shadow: 0 6px 16px rgba(0,0,0,.25);
      transition: transform .12s ease, box-shadow .2s ease, border-color .2s ease;
    }
    .btn:hover { transform: translateY(-1px); box-shadow: 0 10px 22px rgba(0,0,0,.35); border-color: #2a3142; }
    .btn.primary { background: linear-gradient(180deg, #1a543e, #144233); border-color: #1e3a2f; }

    .grid { display: grid; gap: 18px; margin-top: 28px; }
    @media (min-width: 900px){ .grid { grid-template-columns: repeat(12, 1fr); } }

    .card {
      background: linear-gradient(180deg, rgba(17,19,23,.85), rgba(15,17,22,.75));
      border: 1px solid var(--border); border-radius: 16px; padding: 22px; box-shadow: var(--shadow);
    }
    .card h3 { margin: 0 0 8px; font-size: 1.2rem; }
    .muted { color: var(--muted); }

    .list { padding-left: 18px; margin: 8px 0 0; }
    .list li { margin: 6px 0; }

    .section { margin-top: 42px; }
    .section h2 { font-size: 1.6rem; margin: 0 0 10px; }

    .kpis { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 10px; }
    @media (min-width: 700px){ .kpis { grid-template-columns: repeat(4, 1fr); } }
    .kpi { background: #0e1117; border: 1px solid var(--border); border-radius: 12px; padding: 14px; text-align: center; }
    .kpi b { font-size: 1.15rem; }

    .img-grid { display: grid; gap: 10px; grid-template-columns: 1fr; }
    @media (min-width: 820px){ .img-grid { grid-template-columns: repeat(3, 1fr); } }
    .img-grid img { width: 100%; height: 100%; object-fit: cover; border-radius: 14px; border: 1px solid var(--border); }

    pre, code { background: var(--code); border: 1px solid var(--border); border-radius: 10px; padding: 14px; overflow: auto; }

    footer { margin-top: 48px; color: var(--muted); text-align: center; }

    .tag {
      display: inline-block; padding: 6px 10px; border: 1px solid var(--border); border-radius: 999px;
      background: #0e1117; font-size: .9rem; color: var(--muted);
    }

    .two-col { display: grid; gap: 18px; grid-template-columns: 1fr; }
    @media (min-width: 900px){ .two-col { grid-template-columns: 1.5fr 1fr; } }

    .ul-check { list-style: none; padding: 0; margin: 8px 0 0; }
    .ul-check li { margin: 8px 0; display: grid; grid-template-columns: 24px 1fr; gap: 10px; align-items: start; }
    .icon { width: 20px; height: 20px; margin-top: 3px; }
  </style>
</head>
<body>
  <div class="wrap">
    <!-- HERO -->
    <header class="hero">
      <h1 class="title">🎓 Exam Companion</h1>
      <p class="subtitle">Your AI-powered study partner that turns big syllabi into calm, personalized plans.</p>

      <div class="badges">
        <img alt="Made with Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" />
        <img alt="Streamlit" src="https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white" />
        <img alt="OpenAI API" src="https://img.shields.io/badge/AI-OpenAI_API-412991?logo=openai&logoColor=white" />
        <img alt="Hugging Face" src="https://img.shields.io/badge/Hosted_on-HF%20Spaces-FFD21E?logo=huggingface&logoColor=black" />
        <img alt="License" src="https://img.shields.io/badge/License-MIT-green" />
      </div>

      <div class="cta">
        <a class="btn primary" href="https://huggingface.co/spaces/marium-noor-khetran/exam-companion" target="_blank" rel="noopener noreferrer">
          <!-- Play icon -->
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>
          Live Demo
        </a>
        <a class="btn" href="#usage">
          <!-- Rocket icon -->
          <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 13l4 4L19 7"></path></svg>
          Get Started
        </a>
      </div>
    </header>

    <!-- VALUE PROP -->
    <section class="section two-col">
      <div class="card">
        <h2>Why Exam Companion?</h2>
        <ul class="ul-check">
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            Overwhelming syllabus before exams
          </li>
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            Poor time management & procrastination
          </li>
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            Uncertainty about progress leads to stress
          </li>
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            Balancing study with life is hard
          </li>
        </ul>
        <p class="muted" style="margin-top:10px">Without a clear plan, students waste time, lose focus, and feel anxious.</p>
      </div>

      <div class="card">
        <h2>Our Solution</h2>
        <ul class="ul-check">
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="14" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/></svg>
            Parses course material from PDFs or pasted text
          </li>
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Calculates available time by exam date & busy hours
          </li>
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a4 4 0 0 1-4 4H7l-4 4V5a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4z"/></svg>
            Generates a personalized daily schedule with AI
          </li>
          <li>
            <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16l4-4h6a2 2 0 0 0 2-2V4a2 2 0 0 0-2-2z"/></svg>
            Export to PDF or Google Calendar for tracking
          </li>
        </ul>
        <p class="muted" style="margin-top:10px">Result: a realistic, stress-free plan tailored to <b>you</b>.</p>
      </div>
    </section>

    <!-- TECH & QUICK FACTS -->
    <section class="section">
      <div class="grid">
        <div class="card" style="grid-column: span 7;">
          <h2>Tech Stack</h2>
          <ul class="list">
            <li><b>Frontend:</b> Streamlit</li>
            <li><b>Backend:</b> Python, OpenAI API</li>
            <li><b>Deployment / Hosting:</b> Hugging Face Spaces</li>
            <li><b>Libraries & Tools:</b> Claude AI, PyMuPDF, Pandas, DateTime, etc.</li>
          </ul>
        </div>
        <div class="card" style="grid-column: span 5;">
          <h2>Mission</h2>
          <p class="muted">Aligned with <b>Education for All</b>: effective study planning made accessible to anyone with internet access.</p>
          <div class="kpis">
            <div class="kpi"><b>AI-Powered</b><div class="muted">Personalized plans</div></div>
            <div class="kpi"><b>PDF Parsing</b><div class="muted">Upload or paste text</div></div>
            <div class="kpi"><b>Calendar</b><div class="muted">Export & track</div></div>
            <div class="kpi"><b>Lightweight</b><div class="muted">Streamlit app</div></div>
          </div>
        </div>
      </div>
    </section>

    <!-- SCREENSHOTS -->
    <section class="section">
      <h2>Screenshots</h2>
      <div class="img-grid">
        <img src="https://github.com/user-attachments/assets/bc33bc11-8aef-4cdf-945e-efa82fe84581" alt="Dashboard view" />
        <img src="https://github.com/user-attachments/assets/f693d7c0-44da-4c87-8b4f-8b78b840238f" alt="Schedule output" />
        <img src="https://github.com/user-attachments/assets/d7f30af6-a629-4881-a5ca-09de6caec617" alt="PDF Export" />
      </div>
    </section>

    <!-- USAGE -->
    <section id="usage" class="section">
      <h2>How to Use</h2>
      <ol class="list">
        <li>Enter <b>exam date</b>, <b>available hours</b>, and <b>busy hours</b> (sleep, commute, etc.).</li>
        <li>Upload your course content (PDF) or paste text.</li>
        <li>Click <em>Generate</em> to create your AI-powered study plan.</li>
        <li>Download the plan as <b>PDF</b> or export to <b>Google Calendar</b>.</li>
      </ol>
    </section>

    <!-- LIMITATIONS & FUTURE WORK -->
    <section class="section two-col">
      <div class="card">
        <h2>Limitations</h2>
        <ul class="list">
          <li>Rate limits on large PDFs</li>
          <li>Limited customization for daily available hours</li>
        </ul>
      </div>
      <div class="card">
        <h2>Future Work</h2>
        <ul class="list">
          <li>Multi-language support for global accessibility</li>
          <li>Better AI parsing for complex PDFs</li>
          <li>Partial study plans (e.g., topic difficulty weighting)</li>
          <li>Direct Google Calendar API syncing</li>
          <li>Mobile-friendly responsive layout</li>
        </ul>
      </div>
    </section>

    <!-- TEAM -->
    <section class="section">
      <h2>Team</h2>
      <div class="grid">
        <div class="card" style="grid-column: span 4;">
          <h3>Muhammad Haris Khan</h3>
          <p class="muted">Developer (frontend & backend)</p>
          <a class="tag" href="https://github.com/ali-haris" target="_blank" rel="noopener">@ali-haris</a>
        </div>
        <div class="card" style="grid-column: span 4;">
          <h3>Marium Noor Khetran</h3>
          <p class="muted">Deployment / Hosting</p>
          <a class="tag" href="https://github.com/mariumnoorkhetran" target="_blank" rel="noopener">@mariumnoorkhetran</a>
        </div>
        <div class="card" style="grid-column: span 4;">
          <h3>Iram Hameed</h3>
          <p class="muted">Presentation / Documentation</p>
          <a class="tag" href="https://github.com/se-iram" target="_blank" rel="noopener">@se-iram</a>
        </div>
      </div>
    </section>

    <!-- TRACK -->
    <section class="section">
      <h2>Submission Track</h2>
      <p><span class="tag">Education for All</span> — Tools that make learning more accessible, personalized, and engaging for diverse learners.</p>
    </section>

    <footer>
      <p>Built with ❤️ using Python, Streamlit, and OpenAI. Hosted on Hugging Face Spaces.</p>
    </footer>
  </div>
</body>
</html>
