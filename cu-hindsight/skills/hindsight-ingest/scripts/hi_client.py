"""Talking to the Hindsight server, standard library only (US-380 AC3, AC4, AC7a, AC7b,
AC7d, AC9).

Transport rule (AC4): `https://` always; `http://` only when EVERY address the host
resolves to is loopback, or, with `allow_insecure_transport`, a tailnet address. The
resolved address decides, never the name. Over `http://` the connection goes to the very
address that was checked, with the original Host header, so a DNS change between check
and connect cannot redirect it.

Credentials (AC3): `HINDSIGHT_URL` and `HINDSIGHT_API_KEY` come from the environment.
Neither is ever printed, logged or written; errors name the path and the server's
message, never the URL.
"""

from __future__ import annotations

import http.client
import ipaddress
import json
import socket
import ssl
import urllib.parse
from dataclasses import dataclass

URL_VAR, KEY_VAR = "HINDSIGHT_URL", "HINDSIGHT_API_KEY"
TAILNETS = (
    ipaddress.ip_network("100.64.0.0/10"),
    ipaddress.ip_network("fd7a:115c:a1e0::/48"),
)
DETAIL_MAX = 200
PAGE = 100
API = "/v1/default/banks"
REQUIRED_PATHS = (
    ("get", API),
    ("put", API + "/{bank_id}"),
    ("post", API + "/{bank_id}/memories"),
    ("delete", API + "/{bank_id}/documents/{document_id}"),
)


class ClientError(Exception):
    """A refusal or a failed call; `status` is the HTTP status (0: none received)."""

    def __init__(self, message: str, status: int = 0) -> None:
        super().__init__(message)
        self.status = status


@dataclass(frozen=True)
class Endpoint:
    scheme: str
    host: str
    port: int
    prefix: str
    connect_to: str
    host_class: str


def classify(addresses: list) -> str:
    if addresses and all(a.is_loopback for a in addresses):
        return "loopback"
    if addresses and all(any(a in net for net in TAILNETS) for a in addresses):
        return "tailnet"
    return "other"


def _addresses(host: str, port: int, resolver) -> list:
    try:
        infos = resolver(host, port, proto=socket.IPPROTO_TCP)
    except OSError:
        raise ClientError("cannot resolve the server host") from None
    return sorted(
        {ipaddress.ip_address(info[4][0].split("%")[0]) for info in infos}, key=str
    )


def endpoint(url: str, allow_insecure: bool, resolver=socket.getaddrinfo) -> Endpoint:
    """Parse and vet the server URL; raise ClientError before a byte is sent."""
    bad = ClientError(f"{URL_VAR} must be an http(s) URL without credentials")
    try:
        parts = urllib.parse.urlsplit(url)
        port = parts.port or (443 if parts.scheme == "https" else 80)
    except ValueError:
        raise bad from None
    if (
        parts.scheme not in ("http", "https")
        or not parts.hostname
        or "@" in parts.netloc
    ):
        raise bad
    prefix = parts.path.rstrip("/")
    if parts.scheme == "https":
        return Endpoint("https", parts.hostname, port, prefix, parts.hostname, "https")
    addresses = _addresses(parts.hostname, port, resolver)
    kind = classify(addresses)
    if kind == "loopback" or (kind == "tailnet" and allow_insecure):
        return Endpoint("http", parts.hostname, port, prefix, str(addresses[0]), kind)
    hint = (
        " (set allow_insecure_transport for a tailnet host)"
        if kind == "tailnet"
        else ""
    )
    raise ClientError(f"refused: plain http to a {kind} host{hint}; use https")


MISSING = object()  # a 404 the caller said it can live with


def _host_header(host: str, port: int) -> str:
    name = f"[{host}]" if ":" in host else host
    return name if port in (80, 443) else f"{name}:{port}"


def obj(reply, what: str) -> dict:
    """A server reply that must be a JSON object; anything else is a clean error."""
    if not isinstance(reply, dict):
        raise ClientError(f"{what}: unexpected reply from the server")
    return reply


class Client:
    def __init__(self, ep: Endpoint, key: str, timeout: float, connect=None) -> None:
        self.ep, self._key, self.timeout = ep, key, timeout
        self._connect = connect or self._open

    def _open(self):
        if self.ep.scheme == "https":
            ctx = ssl.create_default_context()
            return http.client.HTTPSConnection(
                self.ep.host, self.ep.port, timeout=self.timeout, context=ctx
            )
        return http.client.HTTPConnection(
            self.ep.connect_to, self.ep.port, timeout=self.timeout
        )

    def call(self, method: str, path: str, body=None, ok_missing: bool = False):
        """One request; returns the decoded JSON body (None on 404 when ok_missing)."""
        headers = {
            "Authorization": f"Bearer {self._key}",
            "Content-Type": "application/json",
            "Host": _host_header(self.ep.host, self.ep.port),
        }
        data = json.dumps(body).encode() if body is not None else None
        conn = self._connect()
        try:
            conn.request(method, self.ep.prefix + path, body=data, headers=headers)
            resp = conn.getresponse()
            status, raw = resp.status, resp.read()
        except (OSError, http.client.HTTPException) as exc:
            raise ClientError(
                f"{method} {path}: network error ({type(exc).__name__})"
            ) from None
        finally:
            conn.close()
        if status == 404 and ok_missing:
            return MISSING
        if status >= 400:
            raise ClientError(f"{method} {path}: HTTP {status} {_detail(raw)}", status)
        try:
            return json.loads(raw) if raw else None
        except ValueError:
            raise ClientError(
                f"{method} {path}: unexpected reply from the server"
            ) from None


def _detail(raw: bytes) -> str:
    try:
        detail = json.loads(raw).get("detail", "")
    except (ValueError, AttributeError):
        detail = ""
    return str(detail)[:DETAIL_MAX]


def from_env(
    environ, allow_insecure: bool, timeout: float, resolver=socket.getaddrinfo
) -> Client:
    url, key = environ.get(URL_VAR), environ.get(KEY_VAR)
    if not url or not key:
        raise ClientError(f"{URL_VAR} / {KEY_VAR} are not set in this shell")
    return Client(endpoint(url, allow_insecure, resolver), key, timeout)


def q(value: str) -> str:
    return urllib.parse.quote(value, safe="")


def bank_ids(client: Client) -> set[str]:
    """Every bank on the server, reading all pages (AC7b)."""
    found, offset = set(), 0
    while True:
        page = obj(client.call("GET", f"{API}?limit={PAGE}&offset={offset}"), "banks")
        banks, total = page.get("banks"), page.get("total")
        if not isinstance(banks, list) or not isinstance(total, int):
            raise ClientError("banks: unexpected reply from the server")
        found |= {b.get("bank_id") or b.get("id") for b in banks if isinstance(b, dict)}
        offset += len(banks)
        if not banks or offset >= total:
            return found - {None}


def create_bank(client: Client, bank: str) -> None:
    client.call("PUT", f"{API}/{q(bank)}", {})


def retain(client: Client, bank: str, items: list[dict]) -> str:
    reply = client.call(
        "POST", f"{API}/{q(bank)}/memories", {"items": items, "async": True}
    )
    return str(obj(reply or {}, "retain").get("operation_id") or "")


def delete_document(client: Client, bank: str, note: str) -> bool:
    """True when deleted, False when the server no longer had it (already gone)."""
    path = f"{API}/{q(bank)}/documents/{q(note)}"
    return client.call("DELETE", path, ok_missing=True) is not MISSING


def check(client: Client) -> tuple[str, list[str]]:
    """Server version and the paths this tool needs that the server does not offer."""
    version = obj(client.call("GET", "/version"), "version").get("api_version")
    paths = obj(client.call("GET", "/openapi.json"), "openapi").get("paths")
    if not isinstance(paths, dict):
        raise ClientError("openapi: unexpected reply from the server")
    missing = [
        f"{m.upper()} {p}" for m, p in REQUIRED_PATHS if m not in paths.get(p, {})
    ]
    return str(version or "unknown"), missing
