// packages/core/test/qs_gate.test.ts
import { describe, expect, test, vi } from "vitest";
import {
  computeStateHash,
  processQsGate,
  sha256Hex,
  type GateDeps,
  type Signer,
  type State,
  type Request,
  type CanonicalRequest,
  type ExecutorResult,
  type ArtifactRef,
  type LedgerEntry,
} from "../src/qs_gate";

function deepFreeze<T>(obj: T): T {
  if (!obj || typeof obj !== "object") return obj;
  Object.freeze(obj);
  for (const key of Object.keys(obj as any)) {
    deepFreeze((obj as any)[key]);
  }
  return obj;
}

function makeDeps(overrides?: Partial<GateDeps>): GateDeps {
  const signer: Signer = {
    sign: ({ bodyHash }) => (`sig_${bodyHash}` as any),
  };

  const ledger = {
    append: vi.fn((entry: LedgerEntry) => ({
      newHead: `H_${entry.receiptHash}`,
    })),
  };

  const admissibility = vi.fn((_req: CanonicalRequest, _state: State) => ({ ok: true }));

  const executor = vi.fn((_req: CanonicalRequest, state: State): ExecutorResult => {
    const next: State = {
      ...state,
      data: { ...state.data, counter: ((state.data.counter as number) ?? 0) + 1 },
    };
    const artifacts: ArtifactRef[] = [
      { id: "ACTUATION_PLAN", hash: sha256Hex("plan") },
    ];
    return { newState: next, artifacts };
  });

  const emissionManifests = {
    INCREMENT: { exactArtifactIds: ["ACTUATION_PLAN"] },
    PING: { exactArtifactIds: [] },
  };

  return {
    signer,
    ledger,
    admissibility,
    executor,
    emissionManifests,
    ...overrides,
  };
}

describe("QS-R0/QS-R1: refusal must preserve state hash and ledger head", () => {
  test("NON_CANONICAL_PAYLOAD: undefined in payload => REFUSED; no append; stateHash unchanged", () => {
    const state: State = deepFreeze({
      ledgerHead: "L0",
      policyVersion: "P1",
      data: { counter: 0 },
    });

    const deps = makeDeps();

    const req = {
      requestId: "R1",
      actionType: "PING",
      // payload is intentionally non-canonical at runtime
      payload: { x: undefined },
    } as unknown as Request;

    const before = computeStateHash(state);
    const res = processQsGate(req, state, deps);
    const after = computeStateHash(res.state);

    expect(res.kind).toBe("REFUSED");

    // QS-R0: state preserved
    expect(after).toBe(before);

    // QS-R1: ledger preserved
    expect(res.state.ledgerHead).toBe("L0");
    expect(deps.ledger.append).toHaveBeenCalledTimes(0);

    // Executor/admissibility must not run on canonicalization failure
    expect(deps.admissibility).toHaveBeenCalledTimes(0);
    expect(deps.executor).toHaveBeenCalledTimes(0);

    // Refusal receipt is structured (no filler)
    expect(res.receipt.body.refusal?.reasonCode).toBe("NON_CANONICAL_PAYLOAD");
    expect(res.receipt.ledgerHeadAfter).toBe("L0");
  });

  test("MISSING_WITNESS: admissibility denies => REFUSED; no append; stateHash unchanged", () => {
    const state: State = deepFreeze({
      ledgerHead: "L0",
      policyVersion: "P1",
      data: { counter: 0 },
    });

    const deps = makeDeps({
      admissibility: vi.fn((_req: CanonicalRequest, _s: State) => ({
        ok: false,
        reason: "MISSING_WITNESS",
        message: "Witness quorum is required for this action.",
      })),
    });

    const req: Request = {
      requestId: "R2",
      actionType: "INCREMENT",
      payload: { amount: 1 },
      witness: null,
    };

    const before = computeStateHash(state);
    const res = processQsGate(req, state, deps);
    const after = computeStateHash(res.state);

    expect(res.kind).toBe("REFUSED");
    expect(after).toBe(before); // QS-R0
    expect(res.state.ledgerHead).toBe("L0"); // QS-R1
    expect(deps.ledger.append).toHaveBeenCalledTimes(0);

    // Executor must not run if inadmissible
    expect(deps.executor).toHaveBeenCalledTimes(0);

    expect(res.receipt.body.refusal?.reasonCode).toBe("MISSING_WITNESS");
  });
});

describe("QS-E0: bounded emission must match manifest exactly (fail-closed)", () => {
  test("Executor returns artifact not in manifest => REFUSED; no append; stateHash unchanged", () => {
    const state: State = deepFreeze({
      ledgerHead: "L0",
      policyVersion: "P1",
      data: { counter: 0 },
    });

    const deps = makeDeps({
      // PING expects exactArtifactIds: []
      emissionManifests: { PING: { exactArtifactIds: [] } },
      executor: vi.fn((_req: CanonicalRequest, s: State): ExecutorResult => {
        // returns a newState, but the gate must DISCARD it on QS-E0 failure
        return {
          newState: { ...s, data: { ...s.data, counter: 999 } },
          artifacts: [{ id: "EXTRA_ARTIFACT", hash: sha256Hex("oops") }],
        };
      }),
    });

    const req: Request = {
      requestId: "R3",
      actionType: "PING",
      payload: { ping: true },
    };

    const before = computeStateHash(state);
    const res = processQsGate(req, state, deps);
    const after = computeStateHash(res.state);

    // Fail-closed refusal (not “best effort accept”).
    expect(res.kind).toBe("REFUSED");
    expect(res.receipt.body.refusal?.reasonCode).toBe("EMISSION_MANIFEST_VIOLATION");

    // QS-R0: original state preserved (candidate discarded)
    expect(after).toBe(before);
    expect(res.state.data.counter).toBe(0);

    // QS-R1: ledger unchanged; no append
    expect(res.state.ledgerHead).toBe("L0");
    expect(deps.ledger.append).toHaveBeenCalledTimes(0);
  });

  test("Happy path: manifest matches => EXECUTED; append once; state hash changes and ledger head advances", () => {
    const state: State = deepFreeze({
      ledgerHead: "L0",
      policyVersion: "P1",
      data: { counter: 0 },
    });

    const deps = makeDeps(); // INCREMENT => exactArtifactIds: ["ACTUATION_PLAN"]

    const req: Request = {
      requestId: "R4",
      actionType: "INCREMENT",
      payload: { amount: 1 },
    };

    const before = computeStateHash(state);
    const res = processQsGate(req, state, deps);
    const after = computeStateHash(res.state);

    expect(res.kind).toBe("EXECUTED");
    expect(deps.ledger.append).toHaveBeenCalledTimes(1);

    // State core changed
    expect(after).not.toBe(before);
    expect(res.state.data.counter).toBe(1);

    // Ledger head advanced deterministically via mocked append
    expect(res.state.ledgerHead).toMatch(/^H_/);
    expect(res.receipt.ledgerHeadAfter).toBe(res.state.ledgerHead);
  });
});

describe("QUIESCENT_NOOP: cryptographic accounting of silence", () => {
  test("Null request => QUIESCENT_NOOP; no append; stateHash unchanged", () => {
    const state: State = deepFreeze({
      ledgerHead: "L0",
      policyVersion: "P1",
      data: { counter: 0 },
    });

    const deps = makeDeps();

    const before = computeStateHash(state);
    const res = processQsGate(null, state, deps);
    const after = computeStateHash(res.state);

    expect(res.kind).toBe("QUIESCENT_NOOP");
    expect(after).toBe(before);
    expect(res.state.ledgerHead).toBe("L0");
    expect(deps.ledger.append).toHaveBeenCalledTimes(0);

    // NOOP receipt is still signed/hashed (provable silence)
    expect(res.receipt.body.kind).toBe("QUIESCENT_NOOP");
    expect(res.receipt.bodyHash.length).toBeGreaterThan(0);
    expect(res.receipt.signature.length).toBeGreaterThan(0);
  });
});
