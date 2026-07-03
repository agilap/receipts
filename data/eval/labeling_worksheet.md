# Labeling worksheet — evidence per repo

Write 12 claims per repo in labeled_claims.jsonl: 4 true / 4 stretched / 4 fabricated.
Labels: true | stretched | fabricated. Do not run the pipeline on them until all 60 are written.


## driftwatch

### [metadata](https://github.com/agilap/driftwatch)
GitHub repository driftwatch: no description. Primary language: Python. Topics: none. Created 2026-03-27, last pushed 2026-03-27.

### [languages](https://github.com/agilap/driftwatch)
Languages in repository driftwatch by bytes of code: Python (99%), Mako (0%), Dockerfile (0%).

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
# DriftWatch

![CI](https://github.com/agilap/driftwatch/actions/workflows/ci.yml/badge.svg)

Production model health monitor that detects data drift without requiring labels.

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## What it does

DriftWatch tracks whether a deployed model is seeing data that looks different from what it learned during training.

In the loan risk scenario, a model can look healthy in January and silently degrade by August as applicant income and credit profiles shift. DriftWatch catches that shift early by comparing production feature distributions to a known reference baseline and then surfacing high-impact drift first.

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## Quick Start

```bash
git clone https://github.com/agilap/driftwatch.git
cd driftwatch
cp .env.example .env
docker-compose up
```

API docs: http://localhost:8000/docs

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## Key Concepts

- Reference distribution vs production snapshot:
  Reference data is the baseline (usually training data statistics). Production snapshots are daily (or periodic) batches from live inference traffic. Drift is measured by comparing each snapshot to the reference.
- KS test (Kolmogorov-Smirnov):
  KS checks whether two numeric samples likely came from the same underlying distribution. A low p-value means the production feature shape/location changed significantly.
- PSI (Population Stability Index):
  PSI compares binned proportions between reference and production. It gives an intuitive shift magnitude where higher values indicate stronger population movement.
- JS divergence (Jensen-Shannon):
  JS divergence is a symmetric distance between two probability distributions. It is bounded and stable for both continuous-binned and categorical-style comparisons.
- Weighted drift scoring:
  Not all drift should page the team. DriftWatch multiplies drift magnitude by feature importance so low-business-impact features do not drown out critical ones.
- Health score formula:
  Overall weekly health is computed as:
  `overall_health = 100 × (1 - mean(weighted_scores))`

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## API Reference

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Liveness and version check |
| `POST` | `/models` | Register a monitored model |
| `GET` | `/models` | List monitored models |
| `GET` | `/models/{model_id}` | Fetch one model |
| `POST` | `/models/{model_id}/importances` | Upload feature importances |
| `POST` | `/ingest/reference` | Register reference distribution |
| `GET` | `/ingest/reference/{model_id}` | List reference features |
| `POST` | `/ingest/snapshot` | Ingest production snapshot |
| `GET` | `/ingest/snapshots/{model_id}` | List snapshot dates |
| `GET` | `/ingest/snapshots/{model_id}/{window_date}` | Get snapshot stats for one date |
| `GET` | `/drift/{model_id}/{window_date}` | Get drift scores for one date |
| `GET` | `/drift/{model_id}/latest` | Get latest drift summary |
| `GET` | `/alerts` | List active alerts (`model_id` optional) |
| `GET` | `/alerts/{model_id}` | List alerts for one model |
| `PATCH` | `/alerts/{alert_id}/resolve` | Resolve alert |
| `GET` | `/reports/{model_id}` | List reports for a model |
| `GET` | `/reports/{model_id}/latest` | Get latest weekly report |
| `GET` | `/reports/{model_id}/{week_start}` | Get report for a week |
| `POST` | `/reports/{model_id}/generate` | Manually generate report |

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## Configuration

Environment variables (from `.env.example`):

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `postgresql+asyncpg://driftwatch:driftwatch@localhost:5432/driftwatch` | Async SQLAlchemy connection string |
| `SECRET_KEY` | `changeme-in-production` | App secret for production hardening |
| `ALERT_WEBHOOK_URL` | empty | Optional webhook for alert delivery |
| `REPORT_SCHEDULE_CRON` | `0 0 * * 1` | Weekly report cron (UTC) |
| `LOG_LEVEL` | `INFO` | Global log verbosity |
| `PSI_YELLOW_THRESHOLD` | `0.10` | PSI threshold for yellow severity |
| `PSI_RED_THRESHOLD` | `0.20` | PSI threshold for red severity |
| `KS_PVALUE_THRESHOLD` | `0.05` | KS significance threshold |
| `MIN_SAMPLE_WARNING` | `30` | Warning threshold for low sample size |

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## Running Tests

```bash
docker-compose run api pytest -v
```

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## Architecture

See [architecture.md](architecture.md) for component and data-flow details.

### [readme](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/README.md)
From the README of repository driftwatch:
## Why This Matters

A model can still return predictions while quietly degrading.

In the loan scoring framing: performance that looked like 94% in January can collapse to 71% by August when the input population shifts. DriftWatch is designed to detect this shift early, prioritize critical features, and provide actionable weekly health summaries before business KPIs are materially damaged.

### [dependencies](https://github.com/agilap/driftwatch/blob/feat/ingest-model-registry/requirements.txt)
Dependency file requirements.txt in repository driftwatch declares: alembic, apscheduler, asyncpg, black, fastapi, httpx, numpy, pydantic, pydantic-settings, pytest, pytest-asyncio, ruff, scipy, sqlalchemy, uvicorn.

### [commits](https://github.com/agilap/driftwatch)
Contributor agilap has 12 commits in repository driftwatch.


## vantage

### [metadata](https://github.com/agilap/vantage)
GitHub repository vantage: no description. Primary language: Python. Topics: none. Created 2026-03-26, last pushed 2026-03-31.

### [languages](https://github.com/agilap/vantage)
Languages in repository vantage by bytes of code: Python (100%).

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
# Vantage

Enterprise document intelligence and RAG pipeline for mixed files (PDFs, Excel, emails), built for the Zaigo demo submission.

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## Prerequisites
- Python 3.10+
- Supabase account and project
- OpenAI API key

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## Setup And Run
1. Clone and open the repo:
```bash
git clone <your-repo-url>
cd vantage
```
2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Create your environment file:
```bash
cp .env.example .env
```
5. Update .env values:
- OPENAI_API_KEY: your key (sk-...)
- DATABASE_URL: Supabase transaction pooler URI (port 6543)
- DATABASE_DIRECT_URL: Supabase direct URI (port 5432)
- CHROMA_PATH: local Chroma persistence path (example: ./chroma_db)
- DATA_DIR: data root path (example: ./data)
- POOL_MIN / POOL_MAX: pool sizes
6. Initialize schema in Supabase:
```bash
python db.py
```
7. Launch the app:
```bash
python main.py
```

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
### 10-K PDFs (SEC EDGAR)
- Source: SEC EDGAR browser: https://www.sec.gov/cgi-bin/browse-edgar
- Download annual reports (10-K) for public companies.
- Suggested mix: 5 to 6 companies across sectors, 2 to 6 reports each.

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
### Excel Files
- Export public financial tables (for example from Macrotrends) and save as .xlsx.
- Create a few intentionally messy sheets:
  - merged headers
  - blank rows
  - multiple sheets with one empty sheet

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
### Email Files
- Create plain text files (.txt or .eml) with this structure:
  - Subject: ...
  - From: ...
  - Date: ...
  - blank line
  - body text (2 to 3 paragraphs)
- Include edge cases:
  - one with near-empty body
  - one short thread with multiple From: boundaries

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## Demo Flow
1. Go to Ingest tab.
2. Paste a folder path with your mixed files (or upload multiple files).
3. Click Ingest and watch per-file progress.
4. Go to Query tab.
5. Ask natural language questions.
6. Validate grounded answers using source citations and excerpts.

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## Example Queries
| Query | What it tests |
|-------|---------------|
| What was Apple's total revenue in fiscal year 2023? | Cross-document numeric retrieval (PDF 10-K) |
| Compare gross margins across the ingested 10-K filings. | Multi-document synthesis |
| Which companies mentioned supply chain risk as a key risk factor? | Semantic search across sections |
| What is the net income trend for Microsoft over the last three years? | Time-series extraction from structured text |
| Summarize the email thread about Q3 projections. | Email body retrieval and summarization |
| What does the revenue sheet show for Q2? | Tabular row-group retrieval (Excel) |
| Which filing has the highest R&D spend as a percentage of revenue? | Ratio reasoning across documents |

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## File Map
- architecture.md: system architecture, schema, costs, and scale path.
- cache.py: embedding cache read/write with SHA-256 keys.
- chunk.py: type-aware chunking with token guards.
- config.py: env loading and required configuration constants.
- copilot.md: implementation rules and coding constraints.
- db.py: Supabase pool helpers and schema initialization.
- embed.py: cache-first batch embeddings and Chroma writes.
- extract.py: GPT field extraction and summarization.
- ingest.py: ingest orchestrator for detect/parse/chunk/embed/extract/persist.
- main.py: Gradio UI wiring for ingest and query.
- parse/pdf.py: PDF parsing with scanned fallback.
- parse/excel.py: Excel parsing with merged-cell forward fill.
- parse/email.py: plain text email parsing with skip guards.
- requirements.txt: Python dependencies.
- retrieval.py: retrieval pipeline, grounded answer generation, and query logging.
- retry.py: retry decorator, safe JSON parsing, reusable OpenAI call.
- schema.sql: PostgreSQL schema and indexes.
- seed.py: CLI batch seeding helper that runs ingest_folder.
- states.md: milestone checklist for project states.

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## Latency And Cost (50-100 Documents)
| Stage | Time estimate | Cost estimate |
|---|---|---|
| PDF parsing (50 PDFs, 10 pages avg) | ~15-30s total | $0 |
| Excel parsing (20 files) | ~5s total | $0 |
| Email parsing (30 emails) | ~2s total | $0 |
| Embedding (500 chunks, batch) | ~8-12s | ~$0.004 |
| Field extraction (500 chunks, concurrent) | ~45-90s | ~$0.05-0.10 |
| Query (single) | ~1.5-3s | ~$0.002 |
| Total ingest (100 docs) | ~2-3 min | < $0.15 |

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## Production Delta
For production hardening, move from demo architecture to:
1. pgvector in Supabase instead of local ChromaDB.
2. Celery + Redis for queue-based background ingest and extraction.
3. S3-compatible object storage for raw and processed files.
4. Textract or equivalent OCR pipeline for scanned PDFs at scale.
5. Row Level Security (RLS) with tenant-scoped org_id access controls.

### [readme](https://github.com/agilap/vantage/blob/main/README.md)
From the README of repository vantage:
## Quick Demo Commands
Initialize DB and run UI:
```bash
python db.py
python main.py
```
Run CLI seed ingest for a folder:
```bash
python seed.py ./data/raw
```

### [dependencies](https://github.com/agilap/vantage/blob/main/requirements.txt)
Dependency file requirements.txt in repository vantage declares: chromadb, gradio, odfpy, openai, openpyxl, pandas, pdfplumber, psycopg2-binary, pypdf, python-dotenv, pyxlsb, xlrd.

### [commits](https://github.com/agilap/vantage)
Contributor agilap has 36 commits in repository vantage.


## ISAAC

### [metadata](https://github.com/agilap/ISAAC)
GitHub repository ISAAC: Intelligent Systems for Analyzing, Archiving, and Creating ideas. Primary language: Python. Topics: none. Created 2026-04-25, last pushed 2026-05-02.

### [languages](https://github.com/agilap/ISAAC)
Languages in repository ISAAC by bytes of code: Python (100%).

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
# ISAAC

**Intelligent System for Archiving, Analysis, and Creating**

ISAAC is the local-first bridge between an LLM and your Obsidian vault. Obsidian stays the source of truth; ISAAC sits in the middle as the broker that indexes notes, retrieves relevant memory, compares new ideas against prior work, scores candidates, and writes structured notes back safely.

The product name is **ISAAC**. The Python package, distribution, and CLI intentionally use `isaac_vault` / `isaac-vault` because the plain `isaac` package/command name is already occupied in the Python ecosystem.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## What ISAAC does

- **Connects LLM hosts to Obsidian** through an explicit bridge protocol and MCP tools.
- **Indexes Markdown vaults incrementally** using content hashes, frontmatter, section-aware chunks, and local embeddings.
- **Searches notes with hybrid retrieval** by combining vector similarity with lexical matching.
- **Compares new ideas with citations** so overlap claims point back to specific notes and chunks.
- **Builds LLM-ready context packets and briefs** that combine relevant notes, technologies, idea matches, compare evidence, and write policy.
- **Scores ideas without fake precision** using anchored bands for novelty, build cost, personal fit, and overlap.
- **Writes notes back safely** with templates, atomic writes, `isaac_hash` idempotency, and conflict detection.
- **Runs headless** through a CLI and an MCP stdio server; no web UI or dashboard is required.

The intended product loop is:

```text
LLM host ⇄ ISAAC ⇄ Obsidian vault
```

The LLM should ask ISAAC for context before answering, comparing, or writing. ISAAC returns vault-grounded evidence and safe write instructions; Obsidian remains the human-readable knowledge base.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Repository status

Current implementation package: `isaac_vault`  
Current release line: **v0.4.0**  
Current CLI command: `isaac-vault`  
Default index database: `<vault>/.isaac/isaac.db`

Implemented surfaces include:

- `init`
- `doctor`
- `index` / `index --watch`
- `search`
- `compare`
- `context`
- `brief`
- `protocol`
- `score`
- `shortlist`
- `stats`
- `list`
- `promote`
- `serve` for MCP stdio tools:
  - `vault.search`
  - `vault.compare`
  - `vault.context`
  - `vault.brief`
  - `vault.protocol`
  - `vault.score`
  - `vault.shortlist`
  - `vault.list_notes`
  - `vault.promote_idea`
  - `vault.write_note`
  - `vault.stats`

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for the system design and v1 boundaries.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Requirements

- Python **3.11+**
- [`uv`](https://docs.astral.sh/uv/)
- A local Markdown/Obsidian vault to index

ISAAC defaults to local `sentence-transformers` embeddings with `BAAI/bge-small-en-v1.5`. For smoke tests, demos, CI, or offline setup, use the deterministic hash embedder instead.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Setup

```bash
uv sync
uv run isaac-vault --help
```

Scaffold a vault for first use:

```bash
uv run isaac-vault init /path/to/your/vault
uv run isaac-vault doctor /path/to/your/vault
```

Optional fast/offline mode:

```bash
export ISAAC_EMBEDDING_PROVIDER=deterministic
```

Optional custom local embedding model:

```bash
export ISAAC_EMBEDDING_MODEL="BAAI/bge-small-en-v1.5"
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Quick start

Use deterministic embeddings first if you want a no-download smoke test:

```bash
uv run isaac-vault index /path/to/your/vault --deterministic-embedder
uv run isaac-vault context "flood evacuation dashboard" /path/to/your/vault --deterministic-embedder
uv run isaac-vault brief "flood evacuation dashboard" /path/to/your/vault --deterministic-embedder
uv run isaac-vault search "flood evacuation dashboard" /path/to/your/vault --deterministic-embedder
uv run isaac-vault compare "A dashboard for typhoon evacuation planning" /path/to/your/vault --deterministic-embedder
uv run isaac-vault score "A local-first idea memory for my projects" /path/to/your/vault --deterministic-embedder
uv run isaac-vault stats /path/to/your/vault
```

For production-quality semantic retrieval, omit `--deterministic-embedder` and allow the configured `sentence-transformers` model to load locally:

```bash
uv run isaac-vault index /path/to/your/vault
uv run isaac-vault search "agent memory for project ideas" /path/to/your/vault
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Initialize and diagnose a vault

Create ISAAC's recommended folders plus vault-local starter files under `.isaac/`:

```bash
uv run isaac-vault init /path/to/vault
```

This scaffolds:

- `Ideas/`
- `Projects/`
- `Technologies/`
- `Sources/`
- `.isaac/config.toml`
- `.isaac/templates/idea.md`
- `.isaac/.gitignore`

Run diagnostics without mutating the vault:

```bash
uv run isaac-vault doctor /path/to/vault
```

Use an embedding smoke test when you want to verify the configured model can actually load:

```bash
uv run isaac-vault doctor /path/to/vault --check-embedding-load
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Index a vault

```bash
uv run isaac-vault index /path/to/vault
```

Useful options:

```bash
uv run isaac-vault index /path/to/vault --db /tmp/isaac.db
uv run isaac-vault index /path/to/vault --full
uv run isaac-vault index /path/to/vault --watch --watch-debounce 0.25
uv run isaac-vault index /path/to/vault --deterministic-embedder
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Search indexed notes

```bash
uv run isaac-vault search "portfolio project notes" /path/to/vault --k 10
```

Filter by frontmatter:

```bash
uv run isaac-vault search "flood maps" /path/to/vault --status exploring --type idea --tag disaster-ai
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Compare a new idea

```bash
uv run isaac-vault compare "A coding agent that reads old project notes before proposing new builds" /path/to/vault
```

`compare` returns a structured JSON report with:

- overlap verdict (`low`, `medium`, or `high`)
- cited hits
- retrieved chunks
- a `what_is_new` summary
- a citation-grounded `judgment` that separates duplicate, adjacent, enabling-technology, related-context, and insufficient-evidence cases
- in MCP mode, a host reasoning prompt for final host-side synthesis

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Build an LLM context packet

```bash
uv run isaac-vault context "Can neural operators help flood nowcasting?" /path/to/vault --intent research
```

`context` is the main “middleman” surface. It returns a host-ready packet with:

- the ISAAC bridge protocol version
- an answer-ready brief
- instructions for the LLM host
- relevant vault notes
- relevant technology notes
- relevant idea notes
- optional cited compare evidence
- write-back policy for Obsidian

Supported intents:

```bash
uv run isaac-vault context "new project idea" /path/to/vault --intent compare
uv run isaac-vault context "capture this idea" /path/to/vault --intent write
uv run isaac-vault context "promote TinyTriage" /path/to/vault --intent promote
uv run isaac-vault context "neural operators" /path/to/vault --intent research
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Build a compact answer-ready brief

```bash
uv run isaac-vault brief "Can neural operators help flood nowcasting?" /path/to/vault --intent research
```

`brief` is the compact layer a host LLM should read first. It returns:

- a concise summary
- answer guidance
- technology context
- application/idea context
- citations
- suggested next ISAAC tools

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Show the LLM bridge protocol

```bash
uv run isaac-vault protocol /path/to/vault
```

`protocol` returns static instructions a host model can load before using ISAAC:

- Obsidian is the source of truth.
- ISAAC is the broker for retrieval, compare, and write-back.
- Search/compare before claiming novelty.
- Cite retrieved vault passages.
- Use `vault.write_note` / `vault.promote_idea` instead of raw filesystem writes when possible.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Score an idea

```bash
uv run isaac-vault score "A local MCP server for idea recall" /path/to/vault
```

Rank candidates against each other:

```bash
uv run isaac-vault score "ignored when candidates are supplied" /path/to/vault \
  --candidate "Project memory MCP server" \
  --candidate "Ceramic glaze notebook"
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Shortlist unreviewed ideas

```bash
uv run isaac-vault shortlist /path/to/vault --top 10
```

`shortlist` reviews indexed notes with `type: idea` and `status: unreviewed`, compares each idea against the existing vault while excluding itself, and returns a ranked decision report:

- recommended action: `promote`, `keep`, `merge`, `research-more`, or `archive`
- overlap/novelty/build-cost bands
- ISAAC relevance
- portfolio value
- linked technologies
- cited related notes

Write a Markdown review note back into the vault:

```bash
uv run isaac-vault shortlist /path/to/vault \
  --top 10 \
  --write-report \
  --report-folder "01 Ideas/Reviews"
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### List indexed notes

```bash
uv run isaac-vault list /path/to/vault --type technology
uv run isaac-vault list /path/to/vault --status unreviewed
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Promote an unreviewed idea

Dry-run first:

```bash
uv run isaac-vault promote "TinyTriage" /path/to/vault --folder "02 Projects" --dry-run
```

Write when the rendered output looks right:

```bash
uv run isaac-vault promote "TinyTriage" /path/to/vault --folder "02 Projects"
```

Promotion keeps the source idea note in place, writes an idempotent project note, records `source_idea`, and returns `noop` if the same promotion is repeated.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Show stats and lint

```bash
uv run isaac-vault stats /path/to/vault
```

Stats include note/chunk counts, lint issues, type/status counts, and the database path.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
### Run the MCP server

```bash
uv run isaac-vault serve /path/to/vault
```

Optional explicit database path:

```bash
uv run isaac-vault serve /path/to/vault --db /path/to/vault/.isaac/isaac.db
```

Environment variables recognized by the runtime:

| Variable | Purpose |
| --- | --- |
| `ISAAC_VAULT_PATH` | Default vault path for MCP/runtime configuration |
| `ISAAC_DB_PATH` | Explicit SQLite index path |
| `ISAAC_EMBEDDING_PROVIDER` | `sentence-transformers` or `deterministic` |
| `ISAAC_EMBEDDING_MODEL` | Local sentence-transformers model name |
| `ISAAC_IDEAS_FOLDER` | Default write folder for new ideas |
| `ISAAC_PROJECTS_FOLDER` | Default destination for promoted projects |
| `ISAAC_TECHNOLOGIES_FOLDER` | Convention path for technology/research notes |
| `ISAAC_SOURCES_FOLDER` | Convention path for source/archive notes |

`isaac-vault init` also writes a starter `.isaac/config.toml` documenting these defaults. Runtime behavior currently remains environment/CLI driven, so the config file is a human-editable convention marker rather than a required input.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Codex, Obsidian, and ISAAC

Local Codex filesystem access and ISAAC are separate. Codex can read/write an Obsidian vault directly when the local session has filesystem permission, but that is raw file access. ISAAC is the intentional middleman: it indexes the Markdown vault, stores searchable metadata/embeddings in SQLite, exposes CLI/MCP tools over that index, and returns LLM-ready context packets so the host model can reason from vault evidence instead of guessing.

Use this mental model:

```text
Obsidian = source of truth and human editor
ISAAC    = retrieval, compare, protocol, and safe write-back broker
LLM host = reasoning and conversation layer
```

For LLM integrations, start with `vault.protocol` once per session and `vault.context` or `vault.brief` for each user question or candidate idea. Then call narrower tools (`vault.search`, `vault.compare`, `vault.write_note`, `vault.promote_idea`) as needed.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Vault conventions

ISAAC indexes Markdown files under the vault root and skips common non-content paths such as `.git`, `.obsidian`, `.trash`, `node_modules`, template folders, and daily-note filenames.

Recommended frontmatter:

```yaml
---
title: Project NOAH Flood Map
type: idea
status: exploring
tags: [disaster-ai, maps]
---
```

Important behavior:

- `type` and `status` are linted when missing.
- Frontmatter wins over folder location for note metadata.
- Notes marked with `template: true` are skipped.
- Very large notes are truncated for indexing to keep sync bounded.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Note write-back

`vault.write_note` and the engine writer create Markdown notes with the default idea template at:

```text
isaac_vault/writer/templates/idea.md
```

Write-back is designed to be safe:

- generated filenames are conservative slugs
- writes are atomic
- duplicate content returns `noop`
- existing different content returns `conflict`
- each generated note records an `isaac_hash`

Default write folder: `Ideas/`, or `ISAAC_IDEAS_FOLDER` when using the engine/CLI runtime.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Evaluation and development

Run the deterministic retrieval/compare eval suite:

```bash
uv run python -m isaac_vault.eval.runner --json
```

Validate a real local vault without mutating it:

```bash
uv run python scripts/validate_vault.py /path/to/vault --deterministic
```

Run quality checks:

```bash
uv run ruff check .
uv run mypy isaac_vault tests
uv run pytest
```

Build distributions:

```bash
uv build
```

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Implementation notes

- Storage is SQLite in one file for easy backup and inspection.
- ISAAC uses `sqlite-vec` virtual tables when available and falls back to portable JSON vector tables when the extension cannot be loaded.
- Indexing uses normalized Markdown content hashes, so restored files and misleading mtimes do not silently corrupt sync state.
- Watch mode performs an initial sync, then debounces Markdown filesystem bursts before re-syncing.
- The deterministic embedder is intentionally not semantic; it exists for repeatable tests and offline plumbing checks.

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## Release milestones

- **v0.1.0:** local-first package, indexing, hybrid retrieval, compare, stats, watch mode, deterministic embeddings, and MCP tools.
- **v0.2.0:** vault taxonomy config, note listing, idea promotion, typed compare reports, and real-vault validation.
- **v0.3.0:** ISAAC bridge protocol, context packets, and host-facing workflow guidance.
- **v0.4.0:** answer-ready briefs and citation-grounded compare judgments.

Near-term candidates:

- first-run `init` and local `doctor` release alignment
- stronger vault lint/fix workflow
- expanded real-vault evaluation cases

### [readme](https://github.com/agilap/ISAAC/blob/main/README.md)
From the README of repository ISAAC:
## License

MIT. See [LICENSE](LICENSE).

### [dependencies](https://github.com/agilap/ISAAC/blob/main/pyproject.toml)
Dependency file pyproject.toml in repository ISAAC declares: bm25s, markdown-it-py, mcp, python-frontmatter, sentence-transformers, sqlite-vec, typer, watchdog, xxhash.

### [commits](https://github.com/agilap/ISAAC)
Contributor agilap has 14 commits in repository ISAAC.


## Veritas

### [metadata](https://github.com/agilap/Veritas)
GitHub repository Veritas: Internet posts truth checker. Primary language: Python. Topics: none. Created 2026-03-02, last pushed 2026-03-28.

### [languages](https://github.com/agilap/Veritas)
Languages in repository Veritas by bytes of code: Python (91%), Jupyter Notebook (8%).

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
---
title: TruthScan
emoji: 🔍
colorFrom: red
colorTo: blue
sdk: gradio
sdk_version: "4.20.0"
app_file: app.py
pinned: false
license: mit
short_description: Social Media Fake Post Detector — paste a URL, get the truth
---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
# 🔍 TruthScan — Social Media Fake Post Detector

> Paste a social media post URL → TruthScan scrapes the caption + media → checks if the caption matches the visual content AND if the text itself is credible.

---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
## Supported Platforms

| Platform | URL Format | API Needed? |
|----------|-----------|-------------|
| Instagram | `instagram.com/p/SHORTCODE/` or `instagram.com/reel/SHORTCODE/` | ❌ None (public posts) |
| Facebook | `facebook.com/page/posts/ID` | ❌ None (public posts) |

---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
## Architecture

```
Post URL
   │
   ▼
Layer 0: URL Fetcher
   ├─ detect_platform()     — Instagram / Facebook
   ├─ scrape post           — caption text + media URLs
   └─ download_media()      — save image/video to temp file
   │
   ├─► Layer 1: DistilBERT      — text credibility (LIAR dataset)
   ├─► Layer 2: CLIP ViT-B/32   — caption ↔ image cosine similarity
   ├─► Layer 3: OpenCV + CLIP   — caption ↔ video (keyframe analysis)
   ├─► Layer 4: Wiki + GNews    — source cross-reference
   └─► Layer 5: TinyLlama-1.1B  — plain-English verdict
```

---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
### 1. Clone and install

```bash
git clone https://github.com/agilap/truthscan
cd truthscan
pip install -r requirements.txt
```

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
### 2. Configure API keys

```bash
cp .env.example .env

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
# Then edit .env — add your GNews API key for Layer 4
```

**How to get each key:**

**GNews API key (Layer 4 — optional):**
1. Sign up at https://gnews.io (free tier = 100 req/day)
2. Copy your API key from the dashboard

**Facebook cookies (optional — only for non-public posts):**
1. Install "EditThisCookie" browser extension
2. Log into Facebook → export cookies as JSON
3. Set `FACEBOOK_COOKIES_FILE=/path/to/cookies.json` in .env

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
### 3. Train Layer 1 — one-time, ~10 min on a free Colab T4

Open `train.ipynb` in Google Colab and run all cells. This downloads the LIAR dataset from HuggingFace, fine-tunes DistilBERT, and saves the checkpoint to `./models/liar_distilbert/`.

> **Skip training?** App still works — Layer 1 scores are random until trained, but Layers 0, 2–5 are fully functional.

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
# Opens at http://localhost:7860
```

---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
## Deploy to HuggingFace Spaces

```bash

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
# 1. Create a Gradio Space at https://huggingface.co/spaces

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
#    GNEWS_API_KEY

git remote add space https://huggingface.co/spaces/agilap/truthscan
git push space main
```

To include the trained model:
```bash
git lfs install
git lfs track "models/**"
git add models/ .gitattributes
git commit -m "add trained DistilBERT"
git push space main
```

---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
## File Structure

```
truthscan/
├── app.py                      # Gradio UI — URL input, streaming results
├── train.ipynb                 # DistilBERT training notebook (for Google Colab)
├── requirements.txt
├── .env.example
├── url_fetcher.py              # Layer 0: URL → PostData (caption + media)
├── text_classifier.py          # Layer 1: DistilBERT on LIAR dataset
├── clip_checker.py             # Layer 2: CLIP caption ↔ image
├── video_checker.py            # Layer 3: CLIP caption ↔ video keyframes
├── source_checker.py           # Layer 4: Wikipedia / GNews
└── verdict.py                  # Layer 5: TinyLlama plain-English verdict
```

---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
## Known Limitations

- **Instagram:** Instaloader may be throttled on heavily scraped IPs; works well on HF Spaces
- **Facebook:** Public posts scrape cleanly; friends-only or private posts require cookie auth
- **CLIP thresholds:** Calibrated on MS-COCO — may need tuning for social media imagery
- **TinyLlama:** Small model, occasional hallucinations — treat verdict as a signal, not ground truth

---

### [readme](https://github.com/agilap/Veritas/blob/main/README.md)
From the README of repository Veritas:
## License

MIT — use freely, credit appreciated.

### [dependencies](https://github.com/agilap/Veritas/blob/main/requirements.txt)
Dependency file requirements.txt in repository Veritas declares: accelerate, beautifulsoup4, bitsandbytes, datasets, gradio, open-clip-torch, opencv-python, peft, pillow, python-dotenv, requests, scikit-learn, tavily-python, torch, transformers.

### [commits](https://github.com/agilap/Veritas)
Contributor agilap has 22 commits in repository Veritas.


## clarion

### [metadata](https://github.com/agilap/clarion)
GitHub repository clarion: no description. Primary language: Python. Topics: none. Created 2026-03-25, last pushed 2026-04-19.

### [languages](https://github.com/agilap/clarion)
Languages in repository clarion by bytes of code: Python (100%).

### [readme](https://github.com/agilap/clarion/blob/main/README.md)
From the README of repository clarion:
# Clarion

Clarion is an async meeting intelligence pipeline that transcribes meetings, extracts decisions and action items, retrieves prior context, and exports a report.

### [readme](https://github.com/agilap/clarion/blob/main/README.md)
From the README of repository clarion:
## Prerequisites

- Python 3.10+
- ffmpeg (required by Whisper audio decoding)
- Supabase account (project + Postgres connection strings)
- OpenAI API key

### [readme](https://github.com/agilap/clarion/blob/main/README.md)
From the README of repository clarion:
## Setup and Run

1. Clone the repository and move into it.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create your local env file:

```bash
cp .env.example .env
```

4. Fill in `.env` values for:

- OPENAI_API_KEY
- DATABASE_URL
- DATABASE_DIRECT_URL
- CHROMA_PATH
- WHISPER_MODEL
- POOL_MIN
- POOL_MAX

5. Initialize schema:

```bash
python db.py
```

6. Start the app:

```bash
python main.py
```

### [readme](https://github.com/agilap/clarion/blob/main/README.md)
From the README of repository clarion:
## AMI Corpus (Demo Data)

- Corpus home: https://groups.inf.ed.ac.uk/ami/corpus/
- Download page: https://groups.inf.ed.ac.uk/ami/download
- Suggested session for demo: ES2002a
- Example ES2002a audio (headset mix): https://groups.inf.ed.ac.uk/ami/AMICorpusMirror/amicorpus/ES2002a/audio/ES2002a.Mix-Headset.wav

To seed prior decisions for brief retrieval, process at least 3 meeting wav files:

```bash
python seed.py path/to/meeting1.wav path/to/meeting2.wav path/to/meeting3.wav --topic "project planning"
```

### [readme](https://github.com/agilap/clarion/blob/main/README.md)
From the README of repository clarion:
## Demo Flow

1. Upload an audio file in the UI.
2. Watch status stream through stages.
3. See pre-meeting brief appear (when prior data exists for topic).
4. Review decisions, action items, and follow-up questions.
5. Download the generated markdown report.

### [readme](https://github.com/agilap/clarion/blob/main/README.md)
From the README of repository clarion:
## File Map

- `main.py`: Gradio UI and streaming output wiring.
- `queue.py`: End-to-end async pipeline orchestration.
- `retrieval.py`: Transcription, cleanup, topic extraction, embedding, vector retrieval.
- `reasoning.py`: Prompt chain for classification, actions, summary, follow-ups.
- `action.py`: Database writes, duplicate filtering, pre-meeting brief, report export.
- `db.py`: Supabase connection pool and schema initialization.
- `cache.py`: Embedding cache helpers using Supabase.
- `retry.py`: Async retry decorator and shared OpenAI helpers.
- `config.py`: Environment variable loading and config constants.
- `seed.py`: Sequential batch processor for seeding demo meetings.
- `requirements.txt`: Python dependency list.
- `.env.example`: Documented environment variable template.
- `architecture.md`: System architecture and data flow.
- `copilot.md`: Build constraints and implementation responsibilities.
- `prompts.md`: Prompt library for each model call.
- `states.md`: Project milestone states and current checkpoint.
- `docs/`: Copies of architecture, prompts, states, and copilot docs.

### [dependencies](https://github.com/agilap/clarion/blob/main/requirements.txt)
Dependency file requirements.txt in repository clarion declares: chromadb, gradio, openai, openai-whisper, psycopg2-binary, python-docx, python-dotenv.

### [commits](https://github.com/agilap/clarion)
Contributor agilap has 11 commits in repository clarion.
