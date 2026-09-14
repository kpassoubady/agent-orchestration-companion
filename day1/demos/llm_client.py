"""
Unified LLM client for all course labs.

Students set their provider and API key in `.env`.
All lab exercises import `get_completion()` from this module —
no lab code changes needed when switching providers.

Supported providers:
  - openai   → GPT-4o, GPT-4o-mini
  - gemini   → Gemini 2.5 Flash, Gemini 2.0 Flash
  - claude   → Claude Sonnet 4, Claude Haiku 4.5
  - azure    → Azure-OpenAI-style gateway (custom endpoint + bearer token)

The `azure` provider lets students who only have access to a corporate
gateway (no personal API key) run every lab unchanged. The deployment name,
endpoint, and version are all read from `.env`, so the model can change
without touching any lab code.
"""

import os
import re
from dotenv import load_dotenv
import litellm

# Always prefer current .env values over stale shell variables
# (important for frequently refreshed Azure AD bearer tokens).
load_dotenv(override=True)

# Provider-to-model mapping — instructor configures before class.
# For azure, the deployment names come from .env so they can change freely.
PROVIDER_MODELS = {
    "openai": {
        "default": "gpt-4o",
        "mini": "gpt-4o-mini",
    },
    "gemini": {
        "default": "gemini/gemini-2.5-flash",
        "mini": "gemini/gemini-2.0-flash",
    },
    "claude": {
        "default": "claude-sonnet-4-20250514",
        "mini": "claude-haiku-4-5-20251001",
    },
    "azure": {
        "default": os.getenv("AZURE_DEPLOYMENT_DEFAULT", "gpt-4o"),
        "mini": os.getenv(
            "AZURE_DEPLOYMENT_MINI",
            os.getenv("AZURE_DEPLOYMENT_DEFAULT", "gpt-4o"),
        ),
    },
}

# Embedding model per provider. For azure, the deployment name comes from
# .env (AZURE_DEPLOYMENT_EMBEDDING) so it can change without touching lab code.
PROVIDER_EMBEDDING_MODELS = {
    "openai": "text-embedding-3-small",
    "gemini": "gemini/text-embedding-004",
    "claude": "text-embedding-3-small",  # Anthropic has no native embeddings
    "azure": os.getenv("AZURE_DEPLOYMENT_EMBEDDING", "text-embedding-3-small"),
}

# Read from .env — defaults to openai
PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()


def get_model(tier="default"):
    """Get the model string for the active provider.

    Args:
        tier: "default" for capable model, "mini" for fast/cheap model.

    Returns:
        Model string compatible with litellm.
    """
    models = PROVIDER_MODELS.get(PROVIDER)
    if not models:
        raise ValueError(
            f"Unknown provider '{PROVIDER}'. "
            f"Set LLM_PROVIDER to one of: {list(PROVIDER_MODELS.keys())}"
        )
    name = models.get(tier, models["default"])
    # litellm routes to the gateway when the model is prefixed with "azure/".
    if PROVIDER == "azure" and not name.startswith("azure/"):
        return f"azure/{name}"
    return name


def get_embedding_model():
    """Get the embedding model string for the active provider.

    For azure, the value is read from AZURE_DEPLOYMENT_EMBEDDING in .env and
    prefixed with "azure/" so litellm routes it to the corporate gateway.
    Override any provider's default with the EMBEDDING_MODEL env var.
    """
    name = os.getenv("EMBEDDING_MODEL") or PROVIDER_EMBEDDING_MODELS.get(
        PROVIDER, PROVIDER_EMBEDDING_MODELS["openai"]
    )
    if PROVIDER == "azure" and not name.startswith("azure/"):
        return f"azure/{name}"
    return name


def _azure_api_base():
    """Return the Azure service base URL expected by LiteLLM.
    
    Strips trailing paths like /openai/deployments/... that users often paste
    from the Azure portal.
    """
    api_base = os.getenv("AZURE_API_BASE", "").strip()
    if not api_base:
        return None
    api_base = api_base.split("?", 1)[0].rstrip("/")
    return re.sub(
        r"/openai/deployments/[^/]+/(chat/completions|embeddings)$",
        "",
        api_base,
        flags=re.IGNORECASE,
    )

def _provider_kwargs():
    """Extra litellm kwargs for the active provider.

    For the azure gateway, this supplies the endpoint, API version, and
    bearer token so the request matches the verified Postman call:
        {api_base}/openai/deployments/{deployment}/chat/completions?api-version=...
        Authorization: Bearer <token>
    """
    if PROVIDER == "azure":
        kwargs = {
            "api_base": _azure_api_base(),
            "api_version": os.getenv("AZURE_API_VERSION", "2024-02-01"),
            # azure_ad_token is sent as the "Authorization: Bearer" header.
            # Falls back to AZURE_API_KEY (sent as the "api-key" header) for
            # gateways that expect the standard Azure key instead.
            "azure_ad_token": os.getenv("AZURE_AD_TOKEN"),
            "api_key": os.getenv("AZURE_API_KEY"),
        }
        # Drop unset values so litellm doesn't see a None credential.
        return {k: v for k, v in kwargs.items() if v}
    return {}


def get_completion(messages, tier="default", temperature=0.7, max_tokens=1024, **kwargs):
    """Send a chat completion request to the active LLM provider.

    Args:
        messages: List of message dicts, e.g. [{"role": "user", "content": "Hello"}]
        tier: "default" or "mini" — maps to provider-specific model.
        temperature: Sampling temperature (0.0 - 2.0).
        max_tokens: Maximum tokens in the response.
        **kwargs: Additional parameters passed to litellm.completion().

    Returns:
        The response message content as a string.
    """
    model = get_model(tier)
    response = litellm.completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **_provider_kwargs(),
        **kwargs,
    )
    return response.choices[0].message.content


def get_completion_full(messages, tier="default", temperature=0.7, max_tokens=1024, **kwargs):
    """Same as get_completion() but returns the full response object.

    Useful when students need to inspect usage, finish_reason, etc.
    """
    model = get_model(tier)
    return litellm.completion(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **_provider_kwargs(),
        **kwargs,
    )


def get_embeddings(texts, model=None, **kwargs):
    """Embed a list of texts using the active provider.

    Routes through the same gateway/credentials as chat completions, so Azure
    students who only have a corporate endpoint can embed without a personal
    OpenAI key. See https://docs.litellm.ai/docs/providers/azure/azure_embedding

    Args:
        texts: List of strings to embed.
        model: Optional explicit model string. Defaults to the provider's
            embedding model (Azure deployment for the azure provider).
        **kwargs: Additional parameters passed to litellm.embedding().

    Returns:
        List of embedding vectors (one list of floats per input text).
    """
    model = model or get_embedding_model()
    response = litellm.embedding(
        model=model,
        input=texts,
        **_provider_kwargs(),
        **kwargs,
    )
    return [item["embedding"] for item in response.data]


def show_config():
    """Print the current LLM configuration — useful for lab environment checks."""
    model = get_model("default")
    mini = get_model("mini")
    print(f"Provider:      {PROVIDER}")
    print(f"Default model: {model}")
    print(f"Mini model:    {mini}")
    print(f"Embedding:     {get_embedding_model()}")

    if PROVIDER == "azure":
        print(f"Gateway:       {_azure_api_base() or '⚠️  AZURE_API_BASE not set'}")
        print(f"API version:   {os.getenv('AZURE_API_VERSION', '2024-02-01')}")

    # Check the credential is set (without revealing it)
    key_vars = {
        "openai": "OPENAI_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "claude": "ANTHROPIC_API_KEY",
        "azure": "AZURE_AD_TOKEN",
    }
    key_var = key_vars.get(PROVIDER, "UNKNOWN")
    key_value = os.getenv(key_var, "")
    if not key_value and PROVIDER == "azure":
        key_var, key_value = "AZURE_API_KEY", os.getenv("AZURE_API_KEY", "")
    if key_value:
        print(f"Credential:    {key_var} = ...{key_value[-4:]}")
    else:
        print(f"Credential:    ⚠️  {key_var} is NOT set")


if __name__ == "__main__":
    show_config()
