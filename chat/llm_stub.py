def generate_openai_response(prompt):
    return {
        "provider": "openai",
        "model": "gpt-3.5",
        "response": f"OpenAI: Processed your prompt '{prompt}' with advanced language understanding.\nResponse ID: openai_response_001"
    }

def generate_anthropic_response(prompt):
    return {
        "provider": "anthropic",
        "model": "claude-v1",
        "response": f"Anthropic: Your prompt '{prompt}' has been interpreted ethical AI principles.\nResponse ID: anthropic_response_002"
    }

def generate_gemini_response(prompt):
    return {
        "provider": "gemini",
        "model": "gemini-alpha",
        "response": f"Gemini: Your prompt '{prompt}' was processed using Gemini AI.\nResponse ID: gemini_response_003"
    }

PROVIDER_RESPONSE_MAP = {
    "openai": generate_openai_response,
    "anthropic": generate_anthropic_response,
    "gemini": generate_gemini_response,
}

def get_stub_response(provider, prompt):
    if provider in PROVIDER_RESPONSE_MAP:
        return PROVIDER_RESPONSE_MAP[provider](prompt)
    return {"error": "Provider not found"}
