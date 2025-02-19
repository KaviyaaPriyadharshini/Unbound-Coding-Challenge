import re
from .models import RegexRoutingPolicy

def get_redirect_model(provider: str, model: str, prompt: str):
    """
    Check if the prompt matches any stored regex pattern for the given provider and model.
    If a match is found, return the redirect model. Otherwise, return the original model.
    """
    try:
        # Fetch all regex rules for the given model
        rules = RegexRoutingPolicy.objects.filter(original_model=model)

        for rule in rules:
            if re.search(rule.regex_pattern, prompt, re.IGNORECASE):
                return rule.redirect_model  # Redirect if regex matches

    except Exception as e:
        print(f"Error in regex matching: {e}")

    return model  # Default: Return original model if no match
