from __future__ import annotations

import json
from typing import Any

import pytest

TAS_TELEMETRY_STASH_KEY = pytest.StashKey[dict[str, Any]]()


@pytest.fixture
def tas_telemetry(request: pytest.FixtureRequest) -> dict[str, Any]:
    telemetry: dict[str, Any] = {}
    request.node.stash[TAS_TELEMETRY_STASH_KEY] = telemetry
    return telemetry


def _is_tas_boundary_test(item: pytest.Item) -> bool:
    return bool(
        item.get_closest_marker("topology_safety")
        or item.get_closest_marker("phoenix_recovery")
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not _is_tas_boundary_test(item):
        return

    telemetry = {}
    if TAS_TELEMETRY_STASH_KEY in item.stash:
        telemetry.update(item.stash[TAS_TELEMETRY_STASH_KEY])
    if item.user_properties:
        telemetry.update(dict(item.user_properties))

    payload = {
        "test": item.nodeid,
        "phase": report.when,
        "outcome": report.outcome,
        "telemetry": telemetry,
    }
    telemetry_blob = json.dumps(payload, sort_keys=True, default=str)

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is not None:
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.text(telemetry_blob, name="tas_telemetry"))
        report.extras = extras
        return

    report.sections.append(("tas_telemetry", telemetry_blob))
# Nonce: 91029
