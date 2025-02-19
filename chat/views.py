import json
import os
import re
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ModelProvider, RegexRoutingPolicy, FileUploadRoutingRule
from .utils import get_redirect_model
from django.shortcuts import render
from .llm_stub import get_stub_response
from django.core.files.storage import default_storage


UPLOAD_DIR = "uploads/"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

def get_models(request):
    models = ModelProvider.objects.values_list('provider', 'name')
    formatted_models = [f"{provider}/{name}" for provider, name in models]
    return JsonResponse(formatted_models, safe=False, json_dumps_params={'indent': 4})


@csrf_exempt
def chat_completions(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST requests allowed"}, status=405)

    try:
        data = json.loads(request.body)
        provider = data.get("provider")
        model = data.get("model")
        prompt = data.get("prompt")

        # Validate required fields
        if not provider or not model or not prompt:
            return JsonResponse({"error": "Missing provider, model, or prompt"}, status=400)

        # Check if provider & model exist in DB
        if not ModelProvider.objects.filter(provider=provider, name=model).exists():
            return JsonResponse({"error": "Invalid provider or model"}, status=400)

        # Perform regex-based routing
        final_model = get_redirect_model(provider, model, prompt)  # Imported from utils.py

        # Get stub response using the final model
        response_data = get_stub_response(provider, prompt)

        return JsonResponse({
            "provider": provider,
            "original_model": model,
            "final_model": final_model,
            "response": response_data
        }, json_dumps_params={'indent': 4})

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
def chat_ui(request):
    return render(request, "chat/chat_ui.html")

def admin_portal(request):
    return render(request, "chat/admin_portal.html")

@csrf_exempt
def get_regex_rules(request):
    rules = list(RegexRoutingPolicy.objects.values())
    return JsonResponse({"rules": rules})

@csrf_exempt
def add_regex_rule(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            rule = RegexRoutingPolicy.objects.create(
                regex_pattern=data["regex_pattern"],
                original_model=data["original_model"],
                redirect_model=data["redirect_model"]
            )
            return JsonResponse({"message": "Rule added successfully!"})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_regex_rule(request, rule_id):
    try:
        rule = RegexRoutingPolicy.objects.get(id=rule_id)
        rule.delete()
        return JsonResponse({"message": "Rule deleted successfully!"})
    except RegexRoutingPolicy.DoesNotExist:
        return JsonResponse({"error": "Rule not found"}, status=404)

@csrf_exempt
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        uploaded_file = request.FILES["file"]
        
        # Allow only PDFs
        if not uploaded_file.name.endswith(".pdf"):
            return JsonResponse({"error": "Only PDF files are allowed!"}, status=400)

        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)

        # Save file
        with default_storage.open(file_path, "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({"message": f"✅ File '{uploaded_file.name}' processed successfully!"})
    
    return JsonResponse({"error": "No file uploaded"}, status=400)

from django.http import JsonResponse
from .models import FileRouting

def get_file_routing(request, file_type):
    try:
        route = FileRouting.objects.get(file_type=file_type)
        return JsonResponse({"provider": route.provider, "model": route.model})
    except FileRouting.DoesNotExist:
        return JsonResponse({"error": "No routing found for this file type"}, status=404)
