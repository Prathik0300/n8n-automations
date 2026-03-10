# n8n Automations

A growing collection of production-ready n8n workflows that automate real-world tasks using Claude AI.

## Workflows

| Workflow | Description |
|----------|-------------|
| [Job Application Automator](./workflows/job-application-automator/) | Scrapes jobs daily, tailors resumes and cover letters with AI, compiles PDFs, and tracks applications automatically |

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop) installed and running
- [n8n](https://n8n.io/) instance (self-hosted via Docker or cloud)
- [Anthropic API key](https://console.anthropic.com/)
- Google account (for Sheets, Drive, Docs, Gmail)

## Quick Start

**1. Clone the repo**
```bash
git clone https://github.com/Prathik0300/n8n-automations.git
cd n8n-automations
```

**2. Start n8n**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  --restart always \
  n8nio/n8n
```

Access n8n at `http://localhost:5678`

**3. Pick a workflow and follow its README**

Each workflow folder contains its own setup instructions, required services, and import guide.

## Structure
```
n8n-automations/
├── README.md
├── workflows/
│   └── job-application-automator/
│       ├── workflow.json
│       ├── README.md
│       └── services/
│           ├── latex-compiler/
│           │   ├── Dockerfile
│           │   ├── app.py
│           │   └── fly.toml
│           └── jobspy-api/
│               └── fly.toml
└── docs/
    └── images/
```

## Contributing

Feel free to open a PR with your own workflows following the same folder structure.
