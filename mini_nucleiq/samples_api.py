from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from types import TracebackType

import httpx

from mini_nucleiq.analysis import SampleAnalysis, analyze

DEFAULT_BASE_URL = "https://raw.githubusercontent.com/cellsia/mini-nucleiq-code-challenge/main"
DEFAULT_TIMEOUT = httpx.Timeout(10.0)


@dataclass(frozen=True)
class Sample:
    name: str
    cells: tuple[int, ...]


class SampleFetchError(Exception):
    def __init__(self, name: str, message: str) -> None:
        super().__init__(f"could not retrieve sample {name!r}: {message}")
        self.name = name


class SamplesApiClient:
    def __init__(self, base_url: str = DEFAULT_BASE_URL) -> None:
        self._base_url = base_url.rstrip("/")
        self._client = httpx.Client(timeout=DEFAULT_TIMEOUT)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> SamplesApiClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def fetch(self, name: str) -> Sample:
        url = f"{self._base_url}/samples/{name}.json"
        try:
            response = self._client.get(url)
            response.raise_for_status()
            payload = response.json()
        except httpx.HTTPError as exc:
            raise SampleFetchError(name, str(exc)) from exc

        try:
            return Sample(name=payload["name"], cells=tuple(payload["cells"]))
        except (TypeError, KeyError) as exc:
            raise SampleFetchError(name, "invalid sample payload") from exc


def analyze_sample(name: str, algorithm_names: Sequence[str]) -> SampleAnalysis:
    with SamplesApiClient() as client:
        sample = client.fetch(name)
        return analyze(sample.cells, algorithm_names, sample_name=sample.name)
