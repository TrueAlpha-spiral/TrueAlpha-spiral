/// Canonical SHA-256 hashing — Axiom P₀ (Equivalence).
///
/// `canonical_bytes` sorts field names lexicographically before serialising,
/// so that identical logical content always produces identical byte streams
/// regardless of insertion order.
use sha2::{Digest, Sha256};

/// Compute the SHA-256 digest of an arbitrary byte slice.
#[inline]
pub fn sha256(data: &[u8]) -> [u8; 32] {
    Sha256::digest(data).into()
}

/// Produce a canonical byte string from a list of `(field_name, value_bytes)`
/// pairs.
///
/// Fields are sorted lexicographically by name before concatenation, ensuring
/// that the same logical content always maps to the same hash regardless of
/// the order in which fields were assembled (Axiom P₀).
///
/// Wire format per field:
/// ```text
/// <name_len: u16 LE> <name_bytes> <value_len: u32 LE> <value_bytes>
/// ```
pub fn canonical_bytes(fields: &[(&str, &[u8])]) -> Vec<u8> {
    let mut sorted: Vec<(&str, &[u8])> = fields.to_vec();
    sorted.sort_unstable_by_key(|(name, _)| *name);

    let total = sorted.iter().fold(0usize, |acc, (name, val)| {
        acc + 2 + name.len() + 4 + val.len()
    });
    let mut out = Vec::with_capacity(total);

    for (name, val) in sorted {
        let name_bytes = name.as_bytes();
        out.extend_from_slice(&(name_bytes.len() as u16).to_le_bytes());
        out.extend_from_slice(name_bytes);
        out.extend_from_slice(&(val.len() as u32).to_le_bytes());
        out.extend_from_slice(val);
    }
    out
}

/// Compute the canonical SHA-256 hash of a set of named fields (Axiom P₀).
pub fn canonical_hash(fields: &[(&str, &[u8])]) -> [u8; 32] {
    sha256(&canonical_bytes(fields))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn order_independence() {
        let a = canonical_hash(&[("alpha", b"AAA"), ("beta", b"BBB")]);
        let b = canonical_hash(&[("beta", b"BBB"), ("alpha", b"AAA")]);
        assert_eq!(a, b, "P₀: field order must not affect hash");
    }

    #[test]
    fn different_values_differ() {
        let a = canonical_hash(&[("x", b"1")]);
        let b = canonical_hash(&[("x", b"2")]);
        assert_ne!(a, b);
    }

    #[test]
    fn different_names_differ() {
        let a = canonical_hash(&[("x", b"v")]);
        let b = canonical_hash(&[("y", b"v")]);
        assert_ne!(a, b);
    }

    #[test]
    fn empty_fields() {
        let h = canonical_hash(&[]);
        // SHA-256 of empty byte string is deterministic
        assert_eq!(h, sha256(b""));
    }

    #[test]
    fn stable_digest_regression() {
        // Ensure the wire format does not silently change between builds.
        let h = canonical_hash(&[("gene_id", b"abc"), ("parent", b"def")]);
        // Recompute expected using the documented wire format manually.
        let mut wire = Vec::new();
        // "gene_id" (7 bytes) comes before "parent" (6 bytes) lexicographically
        // ... wait, 'g' > 'p'? No: 'g'=103, 'p'=112 → "gene_id" < "parent"
        wire.extend_from_slice(&(7u16).to_le_bytes()); // "gene_id"
        wire.extend_from_slice(b"gene_id");
        wire.extend_from_slice(&(3u32).to_le_bytes());
        wire.extend_from_slice(b"abc");
        wire.extend_from_slice(&(6u16).to_le_bytes()); // "parent"
        wire.extend_from_slice(b"parent");
        wire.extend_from_slice(&(3u32).to_le_bytes());
        wire.extend_from_slice(b"def");
        assert_eq!(h, sha256(&wire));
    }
}
