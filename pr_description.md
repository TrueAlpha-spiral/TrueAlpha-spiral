Title: 🧪 Add tests for SDFRegistryAPI.register_identity

### 🎯 What
Added missing unit test coverage for `SDFRegistryAPI.register_identity` in `sdf_tas_interface.py`.

### 📊 Coverage
The new test module `tests/test_register_identity.py` covers:
- Registering identity with default empty metadata dictionary.
- Registering identity with custom metadata attributes.
- Confirming shallow copy behavior (mutating the returned dictionary does not mutate the registry entry).
- Overwriting existing sovereign identities in the registry with updated details and metadata.

### ✨ Result
100% test coverage for `register_identity`, ensuring state updates and copy mechanics remain reliable.
