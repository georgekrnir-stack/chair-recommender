import anthropic

from app.config import settings

client = anthropic.Anthropic(api_key=settings.anthropic_api_key)


async def call_llm(system_prompt: str, user_message: str, model: str = "claude-sonnet-4-20250514") -> str:
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )
    return message.content[0].text


async def call_llm_json(system_prompt: str, user_message: str, model: str = "claude-sonnet-4-20250514") -> str:
    """Call LLM expecting JSON output."""
    full_system = system_prompt + "\n\n必ず有効なJSON形式で出力してください。"
    return await call_llm(full_system, user_message, model)
