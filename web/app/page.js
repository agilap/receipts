"use client";

import { useEffect, useState } from "react";
import styles from "./page.module.css";

const VERDICTS = [
  ["supported", "Supported", "Evidence in your repos entails this claim."],
  ["partial", "Partial", "The core is supported; the stated extent is not."],
  ["unsupported", "Unsupported", "Your repo evidence does not back this claim."],
  ["no_evidence", "No evidence", "No repository for this project in the corpus."],
  ["unverifiable", "Unverifiable", "Code evidence cannot decide this kind of claim."],
];

function Claim({ claim }) {
  const [open, setOpen] = useState(false);
  const evidence = claim.evidence || [];
  const core = evidence[0]?.core_variant;
  return (
    <li className={styles.claim}>
      <button className={styles.claimRow} onClick={() => setOpen(!open)}>
        <span className={`${styles.badge} ${styles[claim.verdict]}`}>
          {claim.verdict.replace("_", " ")}
        </span>
        <span className={styles.claimText}>{claim.claim}</span>
        {evidence.length > 0 && (
          <span className={styles.chevron}>{open ? "▾" : "▸"}</span>
        )}
      </button>
      {claim.note && <p className={styles.note}>{claim.note}</p>}
      {core && (
        <p className={styles.note}>
          The core “{core}” is supported; the full claim’s extent is not.
        </p>
      )}
      {open && evidence.length > 0 && (
        <ul className={styles.evidence}>
          {evidence.map((e, i) => (
            <li key={i}>
              <a href={e.url} target="_blank" rel="noreferrer">
                {e.repo} · {e.type}
              </a>
              {"entailment" in e && (
                <span className={styles.score}> entailment {e.entailment}</span>
              )}
              {e.matched_packages && (
                <span className={styles.score}>
                  {" "}
                  declares {e.matched_packages.join(", ")}
                </span>
              )}
              {e.excerpt && <p className={styles.excerpt}>{e.excerpt}</p>}
            </li>
          ))}
        </ul>
      )}
    </li>
  );
}

export default function Home() {
  const [resume, setResume] = useState("");
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch("/api/runs/latest")
      .then((r) => (r.ok ? r.json() : null))
      .then((r) => r && setReport(r))
      .catch(() => {});
  }, []);

  async function verify() {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resume }),
      });
      const body = await res.json();
      if (!res.ok) throw new Error(body.detail || res.statusText);
      setReport(body);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const groups =
    report &&
    VERDICTS.map(([key, label, blurb]) => ({
      key,
      label,
      blurb,
      claims: report.claims.filter((c) => c.verdict === key),
    })).filter((g) => g.claims.length > 0);

  return (
    <main className={styles.main}>
      <header className={styles.header}>
        <h1>Receipts</h1>
        <p>
          Paste your resume. Every claim gets checked against your actual
          GitHub evidence — no verdict without proof.
        </p>
      </header>

      <textarea
        className={styles.paste}
        placeholder="Paste your resume text here…"
        value={resume}
        onChange={(e) => setResume(e.target.value)}
        rows={10}
      />
      <button
        className={styles.verify}
        onClick={verify}
        disabled={loading || resume.trim().length < 100}
      >
        {loading
          ? "Verifying — decomposing claims and running NLI (~30s)…"
          : "Verify"}
      </button>
      {error && <p className={styles.error}>{error}</p>}

      {report && (
        <section>
          <p className={styles.headline}>{report.summary.headline}</p>
          {groups.map((g) => (
            <div key={g.key} className={styles.group}>
              <h2>
                {g.label} <small>({g.claims.length})</small>
              </h2>
              <p className={styles.blurb}>{g.blurb}</p>
              <ul className={styles.claims}>
                {g.claims.map((c, i) => (
                  <Claim key={i} claim={c} />
                ))}
              </ul>
            </div>
          ))}
        </section>
      )}
    </main>
  );
}
