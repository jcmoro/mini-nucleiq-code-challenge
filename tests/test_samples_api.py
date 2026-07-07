import json
from pathlib import Path

import httpx
import pytest
import respx

from mini_nucleiq.samples_api import (
    DEFAULT_BASE_URL,
    SampleFetchError,
    SamplesApiClient,
    analyze_sample,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture(name: str) -> dict:
    return json.loads((FIXTURES / f"{name}.json").read_text())


def _url(name: str) -> str:
    return f"{DEFAULT_BASE_URL}/samples/{name}.json"


@respx.mock
def test_fetch_returns_sample() -> None:
    respx.get(_url("sample-a")).mock(return_value=httpx.Response(200, json=_fixture("sample-a")))

    sample = SamplesApiClient().fetch("sample-a")

    assert sample.name == "sample-a"
    assert sample.cells == (0, 0, 0, 1, 0, 1, 0, 1, 1, 1)


@respx.mock
def test_fetch_raises_on_http_error() -> None:
    respx.get(_url("missing")).mock(return_value=httpx.Response(404))

    with pytest.raises(SampleFetchError):
        SamplesApiClient().fetch("missing")


@respx.mock
def test_fetch_raises_on_malformed_payload() -> None:
    respx.get(_url("weird")).mock(return_value=httpx.Response(200, json={"foo": "bar"}))

    with pytest.raises(SampleFetchError):
        SamplesApiClient().fetch("weird")


@respx.mock
def test_analyze_sample_composes_fetch_and_analysis() -> None:
    respx.get(_url("sample-c")).mock(return_value=httpx.Response(200, json=_fixture("sample-c")))

    analysis = analyze_sample(
        "sample-c",
        ["even-zeroes", "contiguous-ones", "surrounded-ones"],
    )

    assert analysis.sample_name == "sample-c"
    assert analysis.final == "NEGATIVE"


def test_context_manager_closes_client() -> None:
    with SamplesApiClient() as client:
        inner = client._client
    assert inner.is_closed
