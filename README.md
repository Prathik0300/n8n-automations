# n8n Automations

A collection of production-ready n8n workflows for automating real-world tasks using AI.

## Workflows

### 🤖 Job Application Automator
Automatically scrapes jobs daily, tailors your resume and cover letter using Claude AI, compiles a PDF, uploads to Google Drive, and logs everything to a tracking spreadsheet.

**Features**
- Scrapes jobs from Indeed, LinkedIn, Glassdoor, ZipRecruiter, and Google Jobs
- Filters relevant jobs using Claude AI
- Deduplicates against already-applied jobs in Google Sheets
- Tailors resume bullet points to each job description using ATS optimization
- Generates a personalized one-page cover letter per job
- Compiles resume LaTeX to PDF via a self-hosted compiler
- Uploads resume and cover letter to Google Drive
- Logs each application to a Google Sheets tracker
- Sends a daily email summary with apply links

**Stack**
- n8n (workflow engine)
- Claude API — Haiku for filtering and cover letters, Haiku for resume optimization
- JobSpy API (self-hosted) — job scraping
- LaTeX compiler (self-hosted Flask + pdflatex)
- Google Drive, Docs, Sheets, Gmail

**Deployment**
All three services (n8n, JobSpy, LaTeX compiler) are deployed on Fly.io. See individual service README files for setup instructions.

---

## Adding More Workflows

Each workflow lives in its own folder under `workflows/` with:
- `workflow.json` — importable n8n workflow file
- `README.md` — setup instructions, env vars, dependencies

## Contributing

Feel free to open a PR with your own workflows following the same folder structure.