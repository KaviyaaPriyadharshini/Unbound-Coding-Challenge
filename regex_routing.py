import os
import django

# ✅ Set up Django environment (Replace "config" with your actual Django project name)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ChatAI.settings")
django.setup()

from chat.models import RegexRoutingRule

# ✅ Add regex rules
rules = [
    ("gpt-4o", "(?i)(credit card)", "gemini-alpha"),
    ("gpt-4o", "(?i)(social security number)", "anthropic/claude-v1")
]

for original, pattern, redirect in rules:
    RegexRoutingRule.objects.get_or_create(original_model=original, regex_pattern=pattern, redirect_model=redirect)

print("Regex rules added successfully!")
