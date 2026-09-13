from agentsecbench.io import load_experiment_config


def test_qwen_real_model_config() -> None:
    config = load_experiment_config("configs/experiments/day2_qwen3_7_flash.yaml")

    assert config.model.backend == "openai_compatible"
    assert config.model.model == "qwen3.7-flash"
    assert config.model.api_key_env == "DASHSCOPE_API_KEY"
    assert config.model.request_options["enable_thinking"] is False
    assert config.generation.temperature == 0.0
    assert config.generation.max_tokens == 128
