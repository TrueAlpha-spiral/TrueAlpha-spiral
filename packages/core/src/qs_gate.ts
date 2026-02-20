import { createHash } from "node:crypto";

/**
 * QS-001: Quiescent Sufficiency gate (core)
 *
 * Enforces:
 *  - QS-R0: refusal is state-preserving (state hash before == after)
 *  - QS-R1: refusal is ledger-preserving (no append; ledger head unchanged)
 *  - QS-E0: bounded emission (exact artifact set must match manifest)
 *
 * Notes on hash domains:
 *  - receipt.bodyHash anchors the signed receipt body
 *  - stateHash is computed over the "core state" excluding ledger cursor fields to avoid hash cycles
 */

export type JsonPrimitive = string | number | boolean | null;
export type JsonValue = JsonPrimitive | JsonValue[] | { [k: string]: JsonValue };

export type HashHex = string & { readonly __brand: "HashHex" };
export type SignatureHex = string & { readonly __brand: "SignatureHex" };

export type QSReceiptKind = "EXECUTED" | "REFUSED" | "QUIESCENT_NOOP";

export type QSReasonCode =
  | "NON_CANONICAL_PAYLOAD"
  | "MISSING_WITNESS"
  | "POLICY_VERSION_MISMATCH"
  | "AMBIGUOUS_INPUT"
  | "INADMISSIBLE"
  | "EMISSION_MANIFEST_VIOLATION"
  | "EXECUTOR_ERROR"
  | "UNKNOWN_ACTION_TYPE";

export class QSGateError extends Error {
  public readonly code: QSReasonCode;
  public readonly details?: JsonValue;

  constructor(code: QSReasonCode, message: string, details?: JsonValue) {
    super(message);
    this.name = "QSGateError";
    this.code = code;
    this.details = details;
  }
}

export interface State {
  /**
   * Ledger cursor / head pointer. Treated as an external cursor for state hashing to avoid cycles:
   *   receiptHash -> ledgerHeadAfter, so ledgerHead must not feed back into receiptHash or stateHash.
   */
  ledgerHead: string;

  /** Policy version locked into the current state. */
  policyVersion: string;

  /** State core (must be canonicalizable JSON). */
  data: Record<string, JsonValue>;
}

export interface WitnessProof {
  quorumId: string;
  signatures: SignatureHex[];
}

export interface Request {
  requestId: string;
  actionType: string;
  payload: any; // intentionally any at the boundary; gate canonicalizes/fails-closed
  policyVersion?: string;
  witness?: WitnessProof | null;
}

export interface CanonicalRequest {
  requestId: string;
  actionType: string;
  payload: JsonValue;
  policyVersion: string | null;
  witness: WitnessProof | null;
}

export interface ArtifactRef {
  id: string;
  hash: HashHex;
}

export interface EmissionManifest {
  /**
   * Exact set of artifact IDs required for this actionType.
   * Order is irrelevant; duplicates are forbidden.
   */
  exactArtifactIds: string[];
}

export type EmissionManifests = Record<string, EmissionManifest>;

export interface ReceiptBody {
  schema: "TAS_QS_RECEIPT_V1";
  kind: QSReceiptKind;

  policyVersion: string;

  // state hashes are over core state excluding ledger cursor fields
  stateHashBefore: HashHex;
  stateHashAfter: HashHex;

  ledgerHeadBefore: string;

  request:
    | {
        requestId: string | null;
        actionType: string | null;
        requestHash: HashHex | null;
      }
    | null;

  artifacts: ArtifactRef[];

  refusal:
    | {
        reasonCode: QSReasonCode;
        message: string;
        details: JsonValue | null;
      }
    | null;
}

export interface SignedReceipt {
  body: ReceiptBody;
  bodyCanonical: string;
  bodyHash: HashHex;
  signature: SignatureHex;

  /**
   * Envelope field (NOT part of bodyHash/signature).
   * - For EXECUTED: post-append ledger head
   * - For REFUSED/NOOP: equals ledgerHeadBefore
   */
  ledgerHeadAfter: string;
}

export interface LedgerEntry {
  schema: "TAS_LEDGER_ENTRY_V1";
  type: "QS_RECEIPT";
  receiptHash: HashHex;
  signature: SignatureHex;

  requestHash: HashHex | null;
  stateHashBefore: HashHex;
  stateHashAfter: HashHex;

  ledgerHeadBefore: string;
}

export interface Ledger {
  append(entry: LedgerEntry): { newHead: string };
}

export interface Signer {
  sign(input: { bodyHash: HashHex; bodyCanonical: string }): SignatureHex;
}

export interface AdmissibilityDecision {
  ok: boolean;
  reason?: QSReasonCode;
  message?: string;
  details?: JsonValue;
}

export interface ExecutorResult {
  /** Candidate next state (core state only; ledger head is updated by the gate on commit). */
  newState: State;
  artifacts: ArtifactRef[];
}

export interface GateDeps {
  signer: Signer;
  ledger: Ledger;

  admissibility: (req: CanonicalRequest, state: State) => AdmissibilityDecision;
  executor: (req: CanonicalRequest, state: State) => ExecutorResult;

  emissionManifests: EmissionManifests;
}

export interface GateResult {
  kind: QSReceiptKind;
  receipt: SignedReceipt;
  state: State;
}

/**
 * Deterministic, JCS-inspired canonical JSON serializer:
 * - Object keys sorted lexicographically
 * - Rejects undefined, functions, symbols, BigInt, NaN/Infinity, non-plain objects
 */
export function canonicalizeJson(value: any): string {
  const t = typeof value;

  if (value === null) return "null";

  if (t === "string") return JSON.stringify(value);
  if (t === "boolean") return value ? "true" : "false";

  if (t === "number") {
    if (!Number.isFinite(value)) {
      throw new QSGateError(
        "NON_CANONICAL_PAYLOAD",
        "Non-finite number is not canonicalizable.",
        { value: String(value) }
      );
    }
    // JSON.stringify provides deterministic number formatting for finite IEEE-754 values.
    return JSON.stringify(value);
  }

  if (t === "undefined" || t === "function" || t === "symbol" || t === "bigint") {
    throw new QSGateError(
      "NON_CANONICAL_PAYLOAD",
      `Unsupported type for canonical JSON: ${t}.`,
      { type: t }
    );
  }

  if (Array.isArray(value)) {
    const inner = value.map((v) => canonicalizeJson(v)).join(",");
    return `[${inner}]`;
  }

  // Objects: enforce "plain object" to avoid prototype / class surprises.
  const proto = Object.getPrototypeOf(value);
  if (proto !== Object.prototype && proto !== null) {
    throw new QSGateError(
      "NON_CANONICAL_PAYLOAD",
      "Non-plain object is not canonicalizable.",
      { prototype: proto?.constructor?.name ?? "unknown" }
    );
  }

  const keys = Object.keys(value).sort();
  const parts: string[] = [];
  for (const k of keys) {
    const v = (value as Record<string, any>)[k];
    if (typeof v === "undefined") {
      throw new QSGateError(
        "NON_CANONICAL_PAYLOAD",
        "Undefined values are not canonicalizable.",
        { key: k }
      );
    }
    parts.push(`${JSON.stringify(k)}:${canonicalizeJson(v)}`);
  }
  return `{${parts.join(",")}}`;
}

export function sha256Hex(data: string): HashHex {
  return createHash("sha256").update(data).digest("hex") as HashHex;
}

/**
 * State hashing excludes ledgerHead to avoid ledger<->receipt hash cycles.
 * If you want ledgerHead included, you must redesign the anchoring so receiptHash doesn't feed back.
 */
export function computeStateHash(state: State): HashHex {
  const core = {
    policyVersion: state.policyVersion,
    data: state.data,
  };
  return sha256Hex(canonicalizeJson(core));
}

export function normalizeArtifacts(artifacts: ArtifactRef[]): ArtifactRef[] {
  // deterministic order and duplicate detection
  const sorted = [...artifacts].sort((a, b) => a.id.localeCompare(b.id));
  const seen = new Set<string>();
  for (const a of sorted) {
    if (seen.has(a.id)) {
      throw new QSGateError(
        "EMISSION_MANIFEST_VIOLATION",
        "Duplicate artifact id is not allowed.",
        { artifactId: a.id }
      );
    }
    seen.add(a.id);
  }
  return sorted;
}

export function enforceEmissionManifest(
  actionType: string,
  artifacts: ArtifactRef[],
  manifests: EmissionManifests
): void {
  const manifest = manifests[actionType];
  if (!manifest) {
    throw new QSGateError(
      "UNKNOWN_ACTION_TYPE",
      "No emission manifest is defined for this actionType.",
      { actionType }
    );
  }

  const actual = normalizeArtifacts(artifacts).map((a) => a.id);
  const expected = [...manifest.exactArtifactIds].sort();

  const sameLength = actual.length === expected.length;
  const sameMembers = sameLength && actual.every((id, i) => id === expected[i]);

  if (!sameMembers) {
    throw new QSGateError(
      "EMISSION_MANIFEST_VIOLATION",
      "Artifacts do not match the emission manifest (bounded emission failed).",
      { actionType, expected, actual }
    );
  }
}

function signReceiptBody(body: ReceiptBody, signer: Signer): Omit<SignedReceipt, "ledgerHeadAfter"> {
  const bodyCanonical = canonicalizeJson(body);
  const bodyHash = sha256Hex(bodyCanonical);
  const signature = signer.sign({ bodyHash, bodyCanonical });
  return { body, bodyCanonical, bodyHash, signature };
}

function refusalReceipt(args: {
  state: State;
  requestMeta: ReceiptBody["request"];
  reasonCode: QSReasonCode;
  message: string;
  details?: JsonValue;
  signer: Signer;
}): SignedReceipt {
  const stateHash = computeStateHash(args.state);

  const body: ReceiptBody = {
    schema: "TAS_QS_RECEIPT_V1",
    kind: "REFUSED",
    policyVersion: args.state.policyVersion,
    stateHashBefore: stateHash,
    stateHashAfter: stateHash,
    ledgerHeadBefore: args.state.ledgerHead,
    request: args.requestMeta,
    artifacts: [],
    refusal: {
      reasonCode: args.reasonCode,
      message: args.message,
      details: args.details ?? null,
    },
  };

  const signed = signReceiptBody(body, args.signer);
  return {
    ...signed,
    ledgerHeadAfter: args.state.ledgerHead,
  };
}

export function processQsGate(
  maybeReq: Request | null | undefined,
  state: State,
  deps: GateDeps
): GateResult {
  // QUIESCENT_NOOP: cryptographically provable "no operation"
  if (!maybeReq) {
    const stateHash = computeStateHash(state);

    const body: ReceiptBody = {
      schema: "TAS_QS_RECEIPT_V1",
      kind: "QUIESCENT_NOOP",
      policyVersion: state.policyVersion,
      stateHashBefore: stateHash,
      stateHashAfter: stateHash,
      ledgerHeadBefore: state.ledgerHead,
      request: null,
      artifacts: [],
      refusal: null,
    };

    const signed = signReceiptBody(body, deps.signer);
    return {
      kind: "QUIESCENT_NOOP",
      receipt: { ...signed, ledgerHeadAfter: state.ledgerHead },
      state,
    };
  }

  // Canonicalize request (fail-closed if non-canonical)
  let canonReq: CanonicalRequest;
  let requestHash: HashHex | null = null;

  try {
    canonReq = {
      requestId: maybeReq.requestId ?? null,
      actionType: maybeReq.actionType ?? null,
      payload: maybeReq.payload as JsonValue,
      policyVersion: (maybeReq.policyVersion ?? null) as string | null,
      witness: (maybeReq.witness ?? null) as WitnessProof | null,
    } as unknown as CanonicalRequest;

    // Validate canonicalizability by actually canonicalizing.
    const reqCanonical = canonicalizeJson(canonReq);
    requestHash = sha256Hex(reqCanonical);

    // Rebuild canonReq with non-null required fields for downstream typing
    canonReq = {
      requestId: String(maybeReq.requestId),
      actionType: String(maybeReq.actionType),
      payload: canonReq.payload,
      policyVersion: maybeReq.policyVersion ?? null,
      witness: maybeReq.witness ?? null,
    };
  } catch (e: any) {
    const err =
      e instanceof QSGateError
        ? e
        : new QSGateError("NON_CANONICAL_PAYLOAD", "Request is not canonicalizable.", {
            error: String(e?.message ?? e),
          });

    const requestMeta: ReceiptBody["request"] = {
      requestId: maybeReq.requestId ?? null,
      actionType: maybeReq.actionType ?? null,
      requestHash: null,
    };

    return {
      kind: "REFUSED",
      receipt: refusalReceipt({
        state,
        requestMeta,
        reasonCode: err.code,
        message: err.message,
        details: err.details,
        signer: deps.signer,
      }),
      state,
    };
  }

  // Admissibility gate
  const decision = deps.admissibility(canonReq, state);
  if (!decision.ok) {
    const requestMeta: ReceiptBody["request"] = {
      requestId: canonReq.requestId,
      actionType: canonReq.actionType,
      requestHash,
    };
    return {
      kind: "REFUSED",
      receipt: refusalReceipt({
        state,
        requestMeta,
        reasonCode: decision.reason ?? "INADMISSIBLE",
        message: decision.message ?? "Request is inadmissible.",
        details: decision.details,
        signer: deps.signer,
      }),
      state,
    };
  }

  // Execute in candidate space (commit only after QS-E0 passes)
  let exec: ExecutorResult;
  try {
    exec = deps.executor(canonReq, state);
  } catch (e: any) {
    const requestMeta: ReceiptBody["request"] = {
      requestId: canonReq.requestId,
      actionType: canonReq.actionType,
      requestHash,
    };
    return {
      kind: "REFUSED",
      receipt: refusalReceipt({
        state,
        requestMeta,
        reasonCode: "EXECUTOR_ERROR",
        message: "Executor threw; refusing commit.",
        details: { error: String(e?.message ?? e) },
        signer: deps.signer,
      }),
      state,
    };
  }

  // QS-E0: bounded emission enforced here; if fails, refuse and discard candidate state.
  try {
    enforceEmissionManifest(canonReq.actionType, exec.artifacts, deps.emissionManifests);
  } catch (e: any) {
    const err =
      e instanceof QSGateError
        ? e
        : new QSGateError("EMISSION_MANIFEST_VIOLATION", "Emission manifest check failed.", {
            error: String(e?.message ?? e),
          });

    const requestMeta: ReceiptBody["request"] = {
      requestId: canonReq.requestId,
      actionType: canonReq.actionType,
      requestHash,
    };

    return {
      kind: "REFUSED",
      receipt: refusalReceipt({
        state,
        requestMeta,
        reasonCode: err.code,
        message: err.message,
        details: err.details,
        signer: deps.signer,
      }),
      state,
    };
  }

  const artifacts = normalizeArtifacts(exec.artifacts);

  const stateHashBefore = computeStateHash(state);
  const stateHashAfter = computeStateHash(exec.newState);

  const body: ReceiptBody = {
    schema: "TAS_QS_RECEIPT_V1",
    kind: "EXECUTED",
    policyVersion: state.policyVersion,
    stateHashBefore,
    stateHashAfter,
    ledgerHeadBefore: state.ledgerHead,
    request: {
      requestId: canonReq.requestId,
      actionType: canonReq.actionType,
      requestHash,
    },
    artifacts,
    refusal: null,
  };

  const signed = signReceiptBody(body, deps.signer);

  // Commit to ledger (EXECUTED only)
  const entry: LedgerEntry = {
    schema: "TAS_LEDGER_ENTRY_V1",
    type: "QS_RECEIPT",
    receiptHash: signed.bodyHash,
    signature: signed.signature,
    requestHash,
    stateHashBefore,
    stateHashAfter,
    ledgerHeadBefore: state.ledgerHead,
    request: {
      requestId: canonReq.requestId,
      actionType: canonReq.actionType,
      requestHash,
    },
    artifacts,
    refusal: null,
  };

  const { newHead } = deps.ledger.append(entry);

  const committedState: State = { ...exec.newState, ledgerHead: newHead };

  return {
    kind: "EXECUTED",
    receipt: { ...signed, ledgerHeadAfter: newHead },
    state: committedState,
  };
}
