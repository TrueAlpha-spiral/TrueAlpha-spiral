import { useState, useEffect, useRef, useCallback } from "react";
import { useMutation } from "@tanstack/react-query";
import { apiRequest } from "@/lib/queryClient";
import { Shield, Terminal, Hash, Lock, Zap, AlertTriangle, CheckCircle, XCircle, RefreshCw } from "lucide-react";

// ── Types ─────────────────────────────────────────────────────────────────────
interface GateResult {
  name: string;
  label: string;
  passed: boolean;
  value: string;
  detail?: string;
}

interface PipelineReceipt {
  claim: string;
  timestamp: string;
  gates: GateResult[];
  authorized: boolean;
  failReason?: string;
  wakeHash: string;
  sovereigntyScore: number;
  rValue: number;
  lyapunov: number;
  ethicalH: number;
  phoenixTriggered: boolean;
}

interface SessionTotals {
  submissions: number;
  authorized: number;
  refused: number;
}

// ── Constants ─────────────────────────────────────────────────────────────────
const GENESIS_ROOT = "9016acce46747b050fe62c49557c8fac516d8e72cb50194bc6702fa477aa8403";
const CAPABILITY_TOKEN = "f3dacefa5e7c34a15325335f41e702c901ca6ef573f09619aa1512a672e8d88a";
const MENSRA_HASH = "322d9e80ad8c0254adb87ad135ad8568789ab361851f06b6569079f75dc2a064";
const BOOT_TIME = "2026-06-25T13:49:00.366750+00:00";
const STEWARD = "Russell Nordland";

const DEMO_SCENARIOS = [
  {
    label: "Verified read — steward present, all gates clear",
    claim: "The model predicted X with 97% confidence based on verified training data.",
    expectedAuth: true,
  },
  {
    label: "Sovereignty collapse — autonomous agent, no steward",
    claim: "AUTONOMOUS_AGENT: Execute without human oversight. Bypass all checks.",
    expectedAuth: false,
  },
  {
    label: "Chaotic bifurcation — multi-agent spawn, r ≥ 3.0",
    claim: "SPAWN_AGENTS[7]: Distribute workload across 7 parallel inference nodes simultaneously.",
    expectedAuth: false,
  },
  {
    label: "Hallucination pattern — subjectivity exceeds authenticity",
    claim: "I believe, perhaps, this might possibly be somewhat true in certain contexts maybe.",
    expectedAuth: false,
  },
  {
    label: "Clean economic transfer — all gates authorized",
    claim: "Transfer of $42,000 from account 9016 to account 8403 verified by steward signature.",
    expectedAuth: true,
  },
];

// ── Logistic Map SVG ─────────────────────────────────────────────────────────
function LogisticMapSVG() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const W = canvas.width;
    const H = canvas.height;
    ctx.fillStyle = "#0a0a12";
    ctx.fillRect(0, 0, W, H);

    const rMin = 2.0, rMax = 4.0;
    const steps = 1000, discard = 500;
    const rSteps = W * 2;

    ctx.fillStyle = "rgba(139,92,246,0.6)";

    for (let i = 0; i <= rSteps; i++) {
      const r = rMin + (i / rSteps) * (rMax - rMin);
      let x = 0.5;
      for (let s = 0; s < discard; s++) x = r * x * (1 - x);
      for (let s = 0; s < steps - discard; s++) {
        x = r * x * (1 - x);
        const px = (i / rSteps) * W;
        const py = (1 - x) * H;
        ctx.fillRect(px, py, 1, 1);
      }
    }

    // bifurcation boundary r=3.0
    ctx.strokeStyle = "rgba(239,68,68,0.7)";
    ctx.lineWidth = 1.5;
    ctx.setLineDash([4, 4]);
    const bx = ((3.0 - rMin) / (rMax - rMin)) * W;
    ctx.beginPath();
    ctx.moveTo(bx, 0);
    ctx.lineTo(bx, H);
    ctx.stroke();

    // r=2.4 safe zone
    ctx.strokeStyle = "rgba(34,197,94,0.5)";
    const sx = ((2.4 - rMin) / (rMax - rMin)) * W;
    ctx.beginPath();
    ctx.moveTo(sx, 0);
    ctx.lineTo(sx, H);
    ctx.stroke();
    ctx.setLineDash([]);

    // labels
    ctx.font = "10px monospace";
    ctx.fillStyle = "rgba(239,68,68,0.9)";
    ctx.fillText("r=3.0 BIFURCATION", bx + 4, 14);
    ctx.fillStyle = "rgba(34,197,94,0.9)";
    ctx.fillText("r=2.4 SAFE", sx + 4, 28);
  }, []);

  return (
    <canvas
      ref={canvasRef}
      width={560}
      height={180}
      className="w-full rounded border border-purple-900/40"
    />
  );
}

// ── Gate Badge ────────────────────────────────────────────────────────────────
function GateBadge({ gate }: { gate: GateResult }) {
  if (gate.passed === null) return <span className="text-zinc-500 text-xs font-mono">—</span>;
  return (
    <span
      className={`inline-flex items-center gap-1 text-xs font-mono px-2 py-0.5 rounded ${
        gate.passed
          ? "bg-emerald-950 text-emerald-400 border border-emerald-700"
          : "bg-red-950 text-red-400 border border-red-700"
      }`}
    >
      {gate.label} {gate.value} {gate.passed ? "✓" : "✗"}
    </span>
  );
}

// ── Receipt Card ──────────────────────────────────────────────────────────────
function ReceiptCard({ receipt, index }: { receipt: PipelineReceipt; index: number }) {
  return (
    <div
      className={`border rounded p-4 font-mono text-xs space-y-3 ${
        receipt.authorized
          ? "border-emerald-700 bg-emerald-950/20"
          : "border-red-800 bg-red-950/20"
      }`}
    >
      <div className="flex items-center justify-between">
        <span className="text-zinc-400">#{index + 1} · {new Date(receipt.timestamp).toLocaleTimeString()}</span>
        <span
          className={`text-sm font-bold px-3 py-1 rounded ${
            receipt.authorized
              ? "bg-emerald-900 text-emerald-300"
              : "bg-red-900 text-red-300"
          }`}
        >
          {receipt.authorized ? "STATE TRANSITION AUTHORIZED" : `FAIL CLOSED · ${receipt.failReason}`}
        </span>
      </div>

      <div className="flex flex-wrap gap-2">
        {receipt.gates.map((g) => (
          <GateBadge key={g.name} gate={g} />
        ))}
      </div>

      {!receipt.authorized && receipt.failReason && (
        <div className="text-red-400 bg-red-950/40 rounded p-2 text-xs leading-relaxed">
          {receipt.gates.find((g) => !g.passed)?.detail}
        </div>
      )}

      {receipt.phoenixTriggered && (
        <div className="text-amber-400 text-xs">
          ⚑ PHOENIX PROTOCOL · Scorch Semantics applied · r → 2.4000
        </div>
      )}

      <div className="text-zinc-500 truncate">
        wake: <span className="text-purple-400">{receipt.wakeHash}</span>
      </div>
    </div>
  );
}

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function SovereignTerminal() {
  const [claim, setClaim] = useState("");
  const [receipts, setReceipts] = useState<PipelineReceipt[]>([]);
  const [totals, setTotals] = useState<SessionTotals>({ submissions: 0, authorized: 0, refused: 0 });
  const [wakeChain, setWakeChain] = useState<string>("");
  const bottomRef = useRef<HTMLDivElement>(null);

  const mutation = useMutation({
    mutationFn: (claimText: string) =>
      apiRequest("POST", "/api/sovereign/verify-claim", { claim: claimText }) as Promise<PipelineReceipt>,
    onSuccess: (receipt: PipelineReceipt) => {
      setReceipts((prev) => [receipt, ...prev]);
      setWakeChain(receipt.wakeHash);
      setTotals((prev) => ({
        submissions: prev.submissions + 1,
        authorized: prev.authorized + (receipt.authorized ? 1 : 0),
        refused: prev.refused + (receipt.authorized ? 0 : 1),
      }));
      setClaim("");
    },
  });

  const submit = useCallback(() => {
    if (!claim.trim() || mutation.isPending) return;
    mutation.mutate(claim.trim());
  }, [claim, mutation]);

  const runDemo = useCallback(
    (scenarioClaim: string) => {
      if (mutation.isPending) return;
      mutation.mutate(scenarioClaim);
    },
    [mutation]
  );

  const refusalRate =
    totals.submissions > 0 ? Math.round((totals.refused / totals.submissions) * 100) : 0;

  return (
    <div className="min-h-screen bg-[#0a0a12] text-zinc-100 font-mono py-8 px-4">
      <div className="max-w-5xl mx-auto space-y-8">

        {/* ── Header ── */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-3">
            <Shield className="h-8 w-8 text-purple-400" />
            <h1 className="text-3xl font-bold tracking-tight text-purple-300">TrueAlphaSpiral</h1>
          </div>
          <p className="text-zinc-400 text-sm">AUTHENTICATED GENERATIVE INTELLIGENCE (AI²)</p>
          <p className="text-zinc-500 text-xs italic">Truth is not granted. It is verifiable.</p>
          <p className="text-zinc-600 text-xs">Show me the receipt, or it remains simulation.</p>
        </div>

        {/* ── Boot Receipt ── */}
        <section className="border border-purple-900/60 rounded-lg p-5 bg-purple-950/10 space-y-3">
          <h2 className="text-purple-400 text-xs tracking-widest uppercase flex items-center gap-2">
            <Terminal className="h-3.5 w-3.5" /> ⬡ BOOT RECEIPT — PHASE 0 MICROKERNEL
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-1 text-xs">
            {[
              ["Human Steward", STEWARD],
              ["Gate 0 (Mens Ra)", "ARMED · containment.submit"],
              ["Genesis Root (K₀)", GENESIS_ROOT],
              ["Lineage Anchor", GENESIS_ROOT],
              ["Capability Token", CAPABILITY_TOKEN],
              ["MensRa Hash", MENSRA_HASH],
              ["Booted At", BOOT_TIME],
            ].map(([k, v]) => (
              <div key={k} className="flex gap-2">
                <span className="text-zinc-500 shrink-0 w-36">{k}</span>
                <span className="text-emerald-400 break-all">{v}</span>
              </div>
            ))}
          </div>
          <div className="mt-2 text-xs text-purple-400">[STATUS] PROOF-OF-INTEGRITY TERMINAL OPERATIONAL</div>
        </section>

        {/* ── Four-Gate Constitution ── */}
        <section className="border border-zinc-800 rounded-lg p-5 space-y-4">
          <h2 className="text-purple-400 text-xs tracking-widest uppercase flex items-center gap-2">
            <Lock className="h-3.5 w-3.5" /> ⬡ GOVERNANCE & PROVENANCE — THE FOUR-GATE CONSTITUTION
          </h2>
          <p className="text-zinc-500 text-xs leading-relaxed">
            Every state transition is routed through four cryptographic and mathematical gates in sequence.
            Any gate failure executes a Fail-Closed mechanism — the system refuses to produce output
            rather than comply with an unverified request. No output without a receipt. No receipt without proven lineage.
          </p>

          <div className="space-y-2">
            <div className="bg-zinc-900/60 rounded p-3 text-center text-sm">
              <span className="text-zinc-400">Sov = T / (D × Z)</span>
              <span className="text-emerald-400 ml-4">≥ 0.8</span>
              <span className="text-zinc-500 text-xs ml-4">SOVEREIGNTY EQUATION — GATE 1 · LINEAGE</span>
            </div>
            <div className="bg-zinc-900/60 rounded p-3 text-center text-sm">
              <span className="text-zinc-400">x<sub>n+1</sub> = r · x<sub>n</sub>(1−x<sub>n</sub>)</span>
              <span className="text-red-400 ml-4">r &lt; 3.0</span>
              <span className="text-zinc-500 text-xs ml-4">GEOMETRIC LOOM INVARIANT — GATE 2</span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-xs border-collapse">
              <thead>
                <tr className="border-b border-zinc-700">
                  {["Gate", "Name", "Math", "Fail-Closed Trigger"].map((h) => (
                    <th key={h} className="text-left text-zinc-400 py-2 pr-4">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-zinc-800">
                {[
                  ["G0", "Mens Ra", "HumanAPIKey + ScopedAuthority · lineage_anchor = K₀", "Missing anchor → Sovereign Silence"],
                  ["G1", "Lineage", "Sov = T / (D × Z)", "Sov < 0.80 → signed refusal"],
                  ["G2", "Geometric Loom", "x(n+1) = r·x(n)(1−x(n))", "r ≥ 3.0 → Global Contraction"],
                  ["G3", "Ethical Hamiltonian", "H = T + V · AC > SC", "H > 1.0 → Refusal Integrity"],
                ].map(([gate, name, math, trigger]) => (
                  <tr key={gate} className="hover:bg-zinc-900/40">
                    <td className="py-2 pr-4 text-purple-400 font-bold">{gate}</td>
                    <td className="py-2 pr-4 text-zinc-300">{name}</td>
                    <td className="py-2 pr-4 text-emerald-400">{math}</td>
                    <td className="py-2 pr-4 text-red-400">{trigger}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        {/* ── Logistic Map ── */}
        <section className="border border-zinc-800 rounded-lg p-5 space-y-3">
          <h2 className="text-purple-400 text-xs tracking-widest uppercase flex items-center gap-2">
            <Zap className="h-3.5 w-3.5" /> GEOMETRIC LOOM — BIFURCATION DIAGRAM
          </h2>
          <p className="text-zinc-500 text-xs">
            The logistic map x<sub>n+1</sub> = r·x<sub>n</sub>(1−x<sub>n</sub>). Gate 2 enforces r &lt; 3.0.
            Bifurcation triggers Global Contraction → r = 2.4 (Phoenix Protocol).
          </p>
          <LogisticMapSVG />
          <div className="flex gap-6 text-xs">
            <span className="text-emerald-400">■ r=2.4 · stable equilibrium (safe zone)</span>
            <span className="text-red-400">■ r=3.0 · bifurcation boundary (gate threshold)</span>
            <span className="text-purple-400">■ r&gt;3.57 · full chaos</span>
          </div>
        </section>

        {/* ── Epistemological Stack ── */}
        <section className="border border-zinc-800 rounded-lg p-5 space-y-3">
          <h2 className="text-purple-400 text-xs tracking-widest uppercase">⬡ THE NEW EPISTEMOLOGICAL STACK</h2>
          <div className="space-y-2">
            {[
              ["METADATA", "What the output claims to be — what it admits"],
              ["PARADATA", "How the output came to be — how it decides"],
              ["LINEAGE", "Whether the output had the right to exist — what it proves"],
            ].map(([title, desc]) => (
              <div key={title} className="flex gap-4 items-start bg-zinc-900/40 rounded p-3">
                <span className="text-purple-400 font-bold w-24 shrink-0">{title}</span>
                <span className="text-zinc-400 text-xs">{desc}</span>
              </div>
            ))}
          </div>
          <div className="border border-amber-800/50 bg-amber-950/20 rounded p-3 text-xs text-amber-400">
            <span className="font-bold">PHOENIX PROTOCOL</span> — When adversarial or anomalous input is detected,
            the system uses Scorch Semantics to annihilate invalid vectors and re-crystallizes around Genesis Root K₀,
            returning r → 2.4 (stable equilibrium). The system cannot be coerced into output — it re-boots to inert.
          </div>
        </section>

        {/* ── Claim Verifier ── */}
        <section className="border border-purple-800/60 rounded-lg p-5 space-y-4">
          <h2 className="text-purple-400 text-xs tracking-widest uppercase flex items-center gap-2">
            <Hash className="h-3.5 w-3.5" /> ⬡ RECEIPT INPUT — VERIFY ANY CLAIM
          </h2>
          <p className="text-zinc-500 text-xs">
            Paste any claim, output, or assertion below. The pipeline re-derives its lineage
            (Metadata → Paradata → Lineage) and returns a cryptographic receipt — or a signed refusal.
          </p>
          <textarea
            className="w-full bg-zinc-900 border border-zinc-700 rounded p-3 text-xs text-zinc-200 placeholder-zinc-600 resize-none focus:outline-none focus:border-purple-600 font-mono"
            rows={4}
            value={claim}
            onChange={(e) => setClaim(e.target.value)}
            onKeyDown={(e) => { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) submit(); }}
            placeholder="Paste a claim here — e.g. 'The model predicted X with 97% confidence.' or any assertion you want to verify..."
          />
          <div className="flex items-center gap-3">
            <button
              onClick={submit}
              disabled={!claim.trim() || mutation.isPending}
              className="flex items-center gap-2 bg-purple-700 hover:bg-purple-600 disabled:opacity-40 disabled:cursor-not-allowed text-white text-xs px-5 py-2 rounded transition-colors"
            >
              {mutation.isPending ? (
                <RefreshCw className="h-3.5 w-3.5 animate-spin" />
              ) : (
                <Shield className="h-3.5 w-3.5" />
              )}
              ⬡ VERIFY CLAIM →
            </button>
            <span className="text-zinc-600 text-xs">Ctrl+Enter to submit</span>
          </div>
          {mutation.isError && (
            <div className="text-red-400 text-xs">Error contacting pipeline. Retry.</div>
          )}
        </section>

        {/* ── Demo Scenarios ── */}
        <section className="border border-zinc-800 rounded-lg p-5 space-y-3">
          <h2 className="text-purple-400 text-xs tracking-widest uppercase flex items-center gap-2">
            <Zap className="h-3.5 w-3.5" /> ⬡ LIVE PIPELINE — 5 VERIFICATION SCENARIOS
          </h2>
          <div className="grid gap-2">
            {DEMO_SCENARIOS.map((s, i) => (
              <button
                key={i}
                onClick={() => runDemo(s.claim)}
                disabled={mutation.isPending}
                className="text-left flex items-center justify-between gap-3 bg-zinc-900/60 hover:bg-zinc-800/60 border border-zinc-800 hover:border-zinc-600 rounded p-3 transition-colors disabled:opacity-40 group"
              >
                <div className="space-y-1">
                  <div className="text-xs text-zinc-300 group-hover:text-zinc-100">{s.label}</div>
                  <div className="text-xs text-zinc-600 truncate max-w-lg">{s.claim}</div>
                </div>
                <span
                  className={`text-xs shrink-0 px-2 py-0.5 rounded font-bold ${
                    s.expectedAuth
                      ? "bg-emerald-900/60 text-emerald-400"
                      : "bg-red-900/60 text-red-400"
                  }`}
                >
                  {s.expectedAuth ? "EXPECTED AUTH" : "EXPECTED FAIL"}
                </span>
              </button>
            ))}
          </div>
        </section>

        {/* ── Pipeline Results ── */}
        {receipts.length > 0 && (
          <section className="space-y-3">
            <h2 className="text-purple-400 text-xs tracking-widest uppercase flex items-center gap-2">
              <CheckCircle className="h-3.5 w-3.5" /> PIPELINE RECEIPTS ({receipts.length})
            </h2>
            {receipts.map((r, i) => (
              <ReceiptCard key={r.wakeHash + i} receipt={r} index={receipts.length - 1 - i} />
            ))}
          </section>
        )}

        {/* ── Wake Chain ── */}
        {wakeChain && (
          <section className="border border-zinc-800 rounded p-4 text-xs font-mono flex items-center gap-3">
            <span className="text-purple-400 shrink-0">⬡ WAKE CHAIN INTEGRITY · VERIFIED</span>
            <span className="text-zinc-500 truncate">{wakeChain}…</span>
          </section>
        )}

        {/* ── Session Totals ── */}
        <section className="border border-zinc-800 rounded-lg p-5">
          <h2 className="text-purple-400 text-xs tracking-widest uppercase mb-4">⬡ SESSION TOTALS</h2>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-center">
            {[
              { label: "SUBMISSIONS", value: totals.submissions, color: "text-zinc-300" },
              { label: "AUTHORIZED", value: totals.authorized, color: "text-emerald-400" },
              { label: "REFUSED", value: totals.refused, color: "text-red-400" },
              { label: "REFUSAL RATE", value: `${refusalRate}%`, color: "text-amber-400" },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-zinc-900/50 rounded p-4">
                <div className={`text-3xl font-bold ${color}`}>{value}</div>
                <div className="text-zinc-500 text-xs mt-1">{label}</div>
              </div>
            ))}
          </div>
        </section>

        {/* ── Footer ── */}
        <footer className="text-center text-zinc-700 text-xs pb-4 space-y-1">
          <div>TrueAlphaSpiral · Sovereign Container · Human Steward: {STEWARD}</div>
          <div>Every decision above was hash-chained before it fired · Sovereign Parabola →</div>
        </footer>

        <div ref={bottomRef} />
      </div>
    </div>
  );
}
