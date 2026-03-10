# Job Application Automator

Automatically scrapes jobs daily, tailors your resume and cover letter using Claude AI, compiles a PDF, uploads to Google Drive, and logs everything to a tracking spreadsheet — all without manual effort.

## How It Works
```
Daily Trigger (9 PM CT)
  → Scrape jobs from 5 job boards in parallel
  → Filter relevant jobs using Claude AI
  → Deduplicate against Google Sheets tracker
  → Tailor resume LaTeX to each job using Claude
  → Generate personalized cover letter using Claude
  → Compile resume to PDF
  → Upload PDF + cover letter to Google Drive
  → Log application to Google Sheets
  → Send daily email summary with apply links
```

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed and running
- Anthropic API key — get one at [console.anthropic.com](https://console.anthropic.com)
- Google account with access to Sheets, Drive, Docs, and Gmail
- n8n running locally or in the cloud

## Step 1 — Start n8n
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  --restart always \
  n8nio/n8n
```

Access n8n at `http://localhost:5678` and create your owner account.

## Step 2 — Start JobSpy API

JobSpy scrapes jobs from Indeed, LinkedIn, Glassdoor, ZipRecruiter, and Google Jobs.
```bash
docker run -d \
  --name jobspy \
  -p 8000:8000 \
  -e API_KEYS=your_api_key_here \
  -e ENABLE_API_KEY_AUTH=true \
  --restart always \
  rainmanjam/jobspy-api:latest
```

Replace `your_api_key_here` with any string you want — use the same value in the workflow config.

Verify it is running:
```bash
curl -H "x-api-key: your_api_key_here" \
  "http://localhost:8000/api/v1/search_jobs?site_name=indeed&search_term=software+engineer&location=Chicago&results_wanted=1"
```

## Step 3 — Start LaTeX Compiler
```bash
cd workflows/job-application-automator/services/latex-compiler
docker build -t latex-compiler .
docker run -d \
  --name latex-compiler \
  -p 5001:5001 \
  --restart always \
  latex-compiler
```

Verify it is running:
```bash
curl http://localhost:5001/health
```

Should return `{"status": "ok"}`.

## Step 4 — Import the Workflow

1. Open n8n at `http://localhost:5678`
2. Go to **Workflows** → **Add Workflow** → **Import from file**
3. Select `workflow.json` from this folder
4. Click **Import**

## Step 5 — Set Up Google Credentials

In n8n go to **Credentials** → **Add Credential** and add each of these:

| Credential | Type |
|------------|------|
| Google Sheets | Google Sheets OAuth2 API |
| Google Drive | Google Drive OAuth2 API |
| Google Docs | Google Docs OAuth2 API |
| Gmail | Gmail OAuth2 API |

For each one you need a **Client ID** and **Client Secret** from Google Cloud Console:

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project or use an existing one
3. Enable these APIs: Google Sheets, Google Drive, Google Docs, Gmail
4. Go to **Credentials** → **Create Credentials** → **OAuth 2.0 Client ID**
5. Set application type to **Web application**
6. Add `http://localhost:5678/rest/oauth2-credential/callback` to Authorized redirect URIs
7. Copy the Client ID and Secret into n8n

## Step 6 — Configure the Workflow

Open the workflow in n8n and update the **Workflow Config** node:

| Field | Description | Example |
|-------|-------------|---------|
| `spreadsheet_id` | ID from your Google Sheets tracker URL | `1I069177Or9OP4ERaeyDn...` |
| `your_email` | Email to receive daily summary | `you@gmail.com` |
| `max_jobs` | Results per search per site | `5` |
| `location` | Job search location | `United States` |
| `resume_file_id` | Google Drive ID of your base resume | `1h2fi-G8zS2CLOgga1W...` |

## Step 7 — Add Your Resume

Open the **Resume LaTeX Store** node and replace the LaTeX content with your own resume in LaTeX format.

## Step 8 — Add Anthropic API Key

In the **ATS Resume Optimization**, **Filter Jobs with Claude**, and **Write Cover Letter** HTTP nodes, go to **Headers** and replace `YOUR_ANTHROPIC_API_KEY` with your actual key from [console.anthropic.com](https://console.anthropic.com).

## Step 9 — Create Google Sheets Tracker

Create a Google Sheet with a tab named `Application Master` with these exact column headers:
```
Application ID | Company Name | Role Title | Role Type (Intern / FT / Contract) | Location | Work Mode | Job Link | Applied Date | Cover Letter (Y/N) | Referral Name | Recruiter Name | Current Stage | Status | Last Follow-up Date | Salary Range
```

Copy the spreadsheet ID from the URL and paste it into the **Workflow Config** node.

## Step 10 — Activate

Toggle the workflow to **Active** in n8n. It will run automatically every day at 9 PM CT.

To test immediately without waiting, click **Test Workflow** in n8n.

## Deployment to Fly.io (Optional)

To run 24/7 without keeping your laptop on:

**Install flyctl**
```bash
brew install flyctl
fly auth login
```

**Deploy each service**
```bash
cd workflows/job-application-automator/services/latex-compiler
fly deploy

cd workflows/job-application-automator/services/jobspy-api
fly deploy
```

**Update workflow URLs**

After deploying replace the local URLs in your n8n workflow:

| Find | Replace with |
|------|-------------|
| `http://host.docker.internal:8000` | `https://your-jobspy-app.fly.dev` |
| `http://host.docker.internal:5001` | `https://your-latex-app.fly.dev` |

## Cost

| Setup | Cost |
|-------|------|
| Local Docker | Free (laptop must stay on) |
| Fly.io cloud | ~$2-3/month |
| Anthropic API | ~$0.50-1/month depending on job volume |

## Troubleshooting

**LaTeX compiler out of memory** — scale up: `fly scale memory 512 -a your-latex-app`

**Rate limit errors on Claude API** — increase `batchInterval` to `30000` in the HTTP nodes

**No jobs found** — verify JobSpy is running and the API key in Docker matches the one in Workflow Config

**Duplicate jobs in sheet** — the dedup node checks both job URL and company+title combo against existing sheet rows
