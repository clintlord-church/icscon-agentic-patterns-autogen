import os

gpt4o_llm_config = {
    "model": "gpt-4o-2024-08-06", 
    "api_key": os.environ["OPENAI_API_KEY"]
}

gpt4o_mini_llm_config = {
    "model": "gpt-4o-mini-2024-07-18", 
    "api_key": os.environ["OPENAI_API_KEY"]
}

claude_llm_config = {
    "model": "claude-3-5-sonnet-20240620",
    "api_key": os.environ["ANTHROPIC_API_KEY"],
    "api_type": "anthropic"
}

llama31_llm_config = {
    "model": "accounts/fireworks/models/llama-v3p1-405b-instruct", 
    "base_url": "https://api.fireworks.ai/inference/v1/chat/completions",
    "api_key": os.environ["FIREWORKS_API_KEY"]
}

local_phi35_llm_config = {
    "model": "lmstudio-community/Phi-3.5-mini-instruct-GGUF/Phi-3.5-mini-instruct-Q3_K_L.gguf", 
    "base_url": "http://localhost:1234/v1"
}

local_mistral_llm_config = {
    "model": "MaziyarPanahi/Mistral-7B-Instruct-v0.3-GGUF/Mistral-7B-Instruct-v0.3.Q2_K.gguf", 
    "base_url": "http://localhost:1234/v1"
}
