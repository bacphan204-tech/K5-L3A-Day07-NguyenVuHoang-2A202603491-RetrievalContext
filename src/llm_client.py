"""Small OpenAI Responses client; secrets stay out of request/response traces."""
import json
import os
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


def read_settings(env_path=None):
    values = {}
    path = Path(env_path) if env_path is not None else ROOT / ".env"
    if path.is_file():
        for raw in path.read_text(encoding="utf-8-sig").splitlines():
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            name, separator, value = line.partition("=")
            if not separator:
                raise ValueError("Invalid .env line; use NAME=value")
            values[name.strip()] = value.strip().strip('"\'')
    names = ("OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL", "OPENAI_TIMEOUT_SECONDS", "OPENAI_MAX_OUTPUT_TOKENS")
    for name in names:
        if name in os.environ:
            values[name] = os.environ[name]
    key = values.get("OPENAI_API_KEY", "")
    if not key or key.casefold() in ("your_key_here", "replace_me", "sk-..."):
        raise ValueError("Missing OPENAI_API_KEY. Copy .env.example to .env and enter the key locally.")
    base = values.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    parsed = urlparse(base)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("OPENAI_BASE_URL must be an HTTPS base URL without embedded credentials/query")
    model = values.get("OPENAI_MODEL", "gpt-5.4-mini-2026-03-17")
    timeout = int(values.get("OPENAI_TIMEOUT_SECONDS", "120"))
    limit = int(values.get("OPENAI_MAX_OUTPUT_TOKENS", "1500"))
    if not model.strip() or timeout < 1 or limit < 100:
        raise ValueError("Invalid model/timeout/output token limit")
    return {"api_key": key, "base_url": base, "model": model, "timeout_seconds": timeout, "max_output_tokens": limit}


def public_settings(settings):
    return {k: v for k, v in settings.items() if k != "api_key"}


class ResponsesClient:
    def __init__(self, settings):
        self.settings = settings
        self.calls = []
        self.failed_calls = 0

    def call(self, messages, tools, *, force_tool=None):
        body = {"model": self.settings["model"], "input": messages, "tools": tools,
                "tool_choice": {"type": "function", "name": force_tool} if force_tool else "required",
                "parallel_tool_calls": False, "store": False,
                "max_output_tokens": self.settings["max_output_tokens"]}
        # gpt-5.4-mini defaults to no reasoning; omit model-specific parameters.
        request = Request(self.settings["base_url"] + "/responses", data=json.dumps(body).encode("utf-8"),
                          headers={"Authorization": "Bearer " + self.settings["api_key"], "Content-Type": "application/json"})
        started = time.perf_counter()
        try:
            with urlopen(request, timeout=self.settings["timeout_seconds"]) as response:
                result = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            self.failed_calls += 1
            # Error bodies can echo inputs/credentials; report status and provider code only.
            try:
                error = json.loads(exc.read().decode("utf-8"))["error"]
                code = str(error.get("code") or error.get("type") or "request_failed")
            except Exception:
                code = "request_failed"
            code = code.replace(self.settings["api_key"], "[REDACTED]")[:100]
            raise RuntimeError(f"OpenAI HTTP {exc.code}: {code}. Check API key, model access and API billing.") from None
        except (URLError, TimeoutError) as exc:
            self.failed_calls += 1
            raise ConnectionError("OpenAI connection failed or timed out; check internet/proxy and retry.") from None
        self.calls.append({"request": body, "response": result, "elapsed_seconds": time.perf_counter() - started})
        if result.get("status") != "completed":
            raise RuntimeError(f"Model response not completed: {result.get('status')}; check output token limit.")
        calls = [item for item in result.get("output", []) if item.get("type") == "function_call"]
        if len(calls) != 1:
            raise ValueError("Model must return exactly one function call per step")
        call = calls[0]
        args = json.loads(call["arguments"])
        if not isinstance(args, dict):
            raise ValueError("Function arguments must be a JSON object")
        return call, args

    def usage(self):
        inputs = outputs = cached = 0
        for c in self.calls:
            u = c["response"].get("usage", {})
            inputs += u.get("input_tokens", 0)
            outputs += u.get("output_tokens", 0)
            cached += u.get("input_tokens_details", {}).get("cached_tokens", 0)
        known = self.settings["base_url"] == "https://api.openai.com/v1" and self.settings["model"] in ("gpt-5.4-mini", "gpt-5.4-mini-2026-03-17")
        estimated_cost = ((inputs-cached)*0.75 + cached*0.075 + outputs*4.5)/1_000_000 if known and not self.failed_calls else None
        return {"model_calls": len(self.calls), "input_tokens": inputs, "cached_input_tokens": cached,
                "output_tokens": outputs, "failed_calls": self.failed_calls,
                "estimated_api_cost_usd": estimated_cost,
                "cost_note": "Estimate from published standard GPT-5.4-mini token rates, verified 2026-11-14; actual bill may differ. Cost is unknown after a failed request or for an unknown model/endpoint.",
                "pricing_source": "https://developers.openai.com/api/docs/models/gpt-5.4-mini"}
