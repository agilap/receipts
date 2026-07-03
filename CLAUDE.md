# Receipts — working rules
- We work ONE session at a time (see plan below). Never build ahead.
- Before writing code: explain the design in a few sentences and wait for my go.
- After each session: summarize what to manually verify before I commit.
- I write the eval labels and README prose myself. Never generate those.
- Every claim in the README must be true and supported. This project's brand is integrity.

Receipts — Build Plan
One-liner: AI resume tools hallucinate achievements. Receipts verifies every resume claim against your actual GitHub evidence — supported / partial / unsupported, with links to proof.
Origin story (use in README + interviews): An AI nearly shipped a fabricated metric onto my resume. I caught it, then built the tool that catches it automatically. I ran it on myself first.
Mission context: First artifact of "Verified AI" — systems where the LLM narrates only what deterministic evidence supports. Same principle as Mulat's Layer 0/1 design.
Scope (v1, hard boundaries)
In: paste resume text + GitHub username → claim decomposition → per-claim verification → report with evidence links. Single user, no auth, SQLite.
Out (labeled "roadmap" in README, do not build): grounded bullet generation, AST-level skill detection, multi-user/auth, LinkedIn/other evidence sources, gap-analysis coaching.
Architecture

Evidence extraction (ingest/) — GitHub REST API: repos, languages, dependency files (package.json, requirements.txt, lockfiles), READMEs, commit stats. Raw JSON to disk, then normalized into evidence chunks with metadata (repo, type, date, URL)
Claim decomposition — LLM (Haiku-class) splits resume bullets into atomic claims, each typed: tech (verifiable from code), quantitative (usually unverifiable from code → auto-flagged honest "unverifiable"), soft (leadership etc. → unverifiable). Only tech claims proceed to NLI
Verification core — embed evidence chunks locally (bge-m3 on the 3050), retrieve top-k per claim, DeBERTa-v3 NLI (local) for entailment → supported / partial / unsupported, evidence links attached
Report UI — one Next.js page: paste box, verdict list with evidence links, summary stat ("14/22 supported")

Stack: Python FastAPI backend, SQLite, local models via sentence-transformers + HF transformers, Next.js front, docker-compose. LLM cost ≈ $3–5 total.
Eval (the product)
60 labeled claims across ~5 public repos: 20 true / 20 stretched / 20 fabricated. Report precision/recall per verdict class. Headline comparison: fabrication rate of an unconstrained LLM resume-writer vs Receipts on identical inputs. That table + your own resume's report screenshot = README hero.

Schedule (evenings, ~3 weeks alongside Mulat)

Session 1 (~3h): repo init, 5-line README, evidence extraction script for agilap, raw JSON committed
Session 2: claim decomposition prompt + taxonomy; run on your real resume, eyeball quality, iterate until claims are clean atoms
Sessions 3–4: verification core — embeddings, retrieval, NLI, verdict logic. The load-bearing sessions; steal time from UI if needed, never from eval
Session 5: label the 60-claim eval set, run metrics, fix the single worst failure mode only
Session 6: UI page
Session 7: run on your own resume, screenshot, README with eval table, 90-sec demo video
Session 8: deploy (Vercel front + small API host or tunnel-for-video), post to r/PinoyProgrammer + dev Twitter; optional: share in the career-ops Discord as "the verification layer career-ops' disclaimer says you need"

Rules

Verification core before any pixel of UI
No claim ships without a verdict class; "unverifiable" is an honest verdict, not a failure
Every quantitative number in your own README must itself be supported (recursive integrity — it's the brand)
Timebox each session; unfinished polish → roadmap section

Success criteria
Shipped + public repo + eval table with real numbers + your own resume's verification report published + one distribution post. Nothing else counts.