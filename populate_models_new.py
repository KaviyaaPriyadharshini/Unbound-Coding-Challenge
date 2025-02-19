import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatAI.settings") 
django.setup()

from chat.models import ModelProvider
models = [
    ("openai", "gpt-3.5"),
    ("openai", "gpt-4o"),
    ("anthropic", "claude-v1"),
    ("gemini", "gemini-alpha")
]

for provider, model in models:
    ModelProvider.objects.get_or_create(provider=provider, name=model)

print("Models added successfully!")
