from __future__ import annotations

import io
from types import SimpleNamespace
from unittest.mock import patch

from MAS.config import OpenRouterConfig, load_experiment_config
from MAS.llm import OpenRouterLLMClient


def _completion(*, content: str, reasoning: str, tool_call_id: str | None = None):
    calls = []
    if tool_call_id:
        calls.append(
            SimpleNamespace(
                id=tool_call_id,
                type="function",
                function=SimpleNamespace(name="search", arguments='{"query":"test"}'),
            )
        )
    message = SimpleNamespace(
        content=content,
        reasoning_content=reasoning,
        tool_calls=calls,
    )
    return SimpleNamespace(
        choices=[SimpleNamespace(message=message, finish_reason="tool_calls" if calls else "stop")],
        usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5),
    )


class _DeepSeekCompletions:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if len(self.calls) <= 2:
            return _completion(
                content="",
                reasoning=f"reasoning-{len(self.calls)}",
                tool_call_id=f"call_{len(self.calls)}",
            )
        return _completion(content="FINAL ANSWER: done", reasoning="reasoning-3")


def _client() -> OpenRouterLLMClient:
    with patch.dict("os.environ", {"MAS_DISABLE_LIVE_LLM": "1"}):
        return OpenRouterLLMClient(
            OpenRouterConfig(api_key=None, base_url="https://api.deepseek.com"),
            {"default": "deepseek-flash"},
        )


def test_deepseek_config_uses_its_own_key() -> None:
    with patch.dict(
        "os.environ",
        {"DEEPSEEK_API_KEY": "deepseek-test-key", "OPENROUTER_API_KEY": "openrouter-test-key"},
    ):
        config = load_experiment_config("config/manta_deepseek_flash.toml")
    assert config.openrouter.api_key == "deepseek-test-key"
    assert config.models["default"] == "deepseek-flash"


def test_deepseek_request_omits_openrouter_fields() -> None:
    client = _client()
    with patch.dict("os.environ", {"DEEPSEEK_REASONING_EFFORT": "medium", "DEEPSEEK_THINKING": "enabled"}):
        request = client._apply_openrouter_sampling_overrides(
            {"model": "deepseek-flash", "max_tokens": None}, temperature=0.0
        )
        request = client._apply_openrouter_routing_overrides(request)
    assert request["reasoning_effort"] == "medium"
    assert request["extra_body"] == {"thinking": {"type": "enabled"}}
    assert "provider" not in request["extra_body"]
    assert "top_k" not in request["extra_body"]
    assert "temperature" not in request


def test_deepseek_tool_loop_preserves_all_reasoning_turns() -> None:
    client = _client()
    completions = _DeepSeekCompletions()
    client.client = SimpleNamespace(chat=SimpleNamespace(completions=completions))
    with patch.dict(
        "os.environ",
        {"MAS_TOOL_CONTEXT_RAW_TURNS": "1", "DEEPSEEK_THINKING": "enabled"},
    ):
        result = client.generate(
            prompt="Find the answer",
            agent_type="default",
            task_id="t1",
            run_index=0,
            agent_id="agent_0",
            tools=[
                {
                    "name": "search",
                    "description": "Search",
                    "parameters": {
                        "type": "object",
                        "properties": {"query": {"type": "string"}},
                        "required": ["query"],
                    },
                    "handler": lambda args: {"result": args["query"]},
                }
            ],
            max_tool_iterations=3,
        )
    assert result.text == "FINAL ANSWER: done"
    assert len(completions.calls) == 3
    third_messages = completions.calls[2]["messages"]
    assert [m["reasoning_content"] for m in third_messages if m.get("role") == "assistant"] == [
        "reasoning-1",
        "reasoning-2",
    ]
    assert completions.calls[2]["extra_body"] == {"thinking": {"type": "enabled"}}
    assert result.metadata["provider"] == "deepseek"


def test_llm_logging_survives_legacy_windows_output_encoding() -> None:
    raw = io.BytesIO()
    output = io.TextIOWrapper(raw, encoding="cp1252", errors="strict")
    with patch("sys.stdout", output):
        OpenRouterLLMClient._log("tool snippet: Ş ı ′")
    assert raw.getvalue().decode("ascii").strip() == (
        r"[llm] tool snippet: \u015e \u0131 \u2032"
    )
