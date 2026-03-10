# Job Application Automator

Automatically applies to jobs daily with AI-tailored resumes and cover letters.

## Architecture
```
Daily Trigger (9 PM CT)
  → Fetch Jobs (JobSpy API — 5 sites, 18 search terms, parallel batching)
  → Filter with Claude AI (relevant tech jobs only)
  → Deduplicate against Google Sheets tracker
  → Build ATS-optimized resume prompt per job
  → Call Claude API to tailor resume LaTeX
  → Sanitize LaTeX + build cover letter prompt
  → Call Claude API to write cover letter
  → Merge all data
  → Compile LaTeX to PDF
  → Upload PDF to Google Drive
  → Create cover letter Google Doc
  → Log to Google Sheets tracker
  → Send email summary
```

## Prerequisites

- n8n instance (self-hosted or cloud)
- Anthropic API key
- Google Cloud OAuth credentials (Sheets, Drive, Docs, Gmail)
- JobSpy API (self-hosted)
- LaTeX compiler service (self-hosted)

## Setup

**1. Deploy services**

Deploy JobSpy and LaTeX compiler to Fly.io:
```bash
cd services/latex-compiler && fly deploy
cd services/jobspy-api && fly deploy
```

**2. Import workflow**

In n8n → Workflows → Import → select `workflow.json`

**3. Configure credentials**

Add these credentials in n8n:
- Anthropic API key (HTTP Header Auth)
- Google Sheets OAuth2
- Google Drive OAuth2
- Google Docs OAuth2
- Gmail OAuth2

**4. Update Workflow Config node**

| Field | Description |
|-------|-------------|
| `spreadsheet_id` | Google Sheets tracker ID |
| `resume_file_id` | Google Drive resume file ID |
| `your_email` | Email to send daily summary to |
| `max_jobs` | Results per search term per site |
| `location` | Job search location |

**5. Update Resume LaTeX Store node**

Replace the LaTeX content with your own resume.

**6. Activate**

Toggle the workflow to Active in n8n. Runs daily at 9 PM CT.

## Services

| Service | Description | Port |
|---------|-------------|------|
| JobSpy API | Scrapes jobs from major job boards | 8000 |
| LaTeX Compiler | Compiles LaTeX resume to PDF | 5001 |

## Cost

~$2-3/month on Fly.io (n8n at 512MB, others at 256MB with auto-sleep)