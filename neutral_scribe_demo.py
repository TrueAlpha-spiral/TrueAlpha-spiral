from neutral_scribe import NeutralScribe


def main() -> None:
    scribe = NeutralScribe(
        spec_id="TAS-PSVP-2026-abcd1234",
        axiom_set_hash="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        invariant_set_hash="bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    )

    s_t = {
        "spec_id": "TAS-PSVP-2026-abcd1234",
        "axiom_set_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "invariant_set_hash": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "axioms": "dayzero-core",
        "payload": "s0",
    }

    s_tp1 = {
        "spec_id": "TAS-PSVP-2026-abcd1234",
        "axiom_set_hash": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "invariant_set_hash": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
        "axioms": "dayzero-core",
        "payload": "s1",
    }

    bundle = scribe.scribe(s_t, s_tp1)
    print(bundle)


if __name__ == "__main__":
    main()
