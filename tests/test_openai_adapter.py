from agentsecbench.adapters.openai_compatible import OpenAICompatibleAdapter
from agentsecbench.cli import build_adapter
from agentsecbench.schema import ModelConfig


def test_openai_adapter_can_disable_environment_proxy() -> None:
    config = ModelConfig(
        backend="openai_compatible",
        model="test-model",
        base_url="https://example.invalid/v1",
        trust_env=False,
    )

    adapter = build_adapter(config)

    assert isinstance(adapter, OpenAICompatibleAdapter)
    assert adapter.trust_env is False
