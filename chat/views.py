import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import ModelProvider, RegexRoutingPolicy, FileUploadRouting
from .utils import get_redirect_model
from .llm_stub import get_stub_response

def sign_in(request):
    return render(request, 'chat/signin.html')

def admin_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_portal')
        else:
            messages.error(request, "Invalid admin credentials")
    return render(request, 'chat/admin_login.html')

def user_dashboard(request):
    return render(request, 'chat/user_dashboard.html')

def user_logout(request):
    logout(request)
    return redirect('sign_in')

def get_models(request):
    models = ModelProvider.objects.values_list("provider", "name")
    formatted_models = [f"{provider}/{name}" for provider, name in models]
    return JsonResponse(formatted_models, safe=False, json_dumps_params={"indent": 4})

@csrf_exempt
@require_POST
def chat_completions(request):
    try:
        data = json.loads(request.body)
        provider, model, prompt = data.get("provider"), data.get("model"), data.get("prompt")

        if not provider or not model or not prompt:
            return JsonResponse({"error": "Missing provider, model, or prompt"}, status=400)

        if not ModelProvider.objects.filter(provider=provider, name=model).exists():
            return JsonResponse({"error": "Invalid provider or model"}, status=400)

        final_model = get_redirect_model(provider, model, prompt)  
        response_data = get_stub_response(provider, prompt)

        return JsonResponse({
            "provider": provider,
            "original_model": model,
            "final_model": final_model,
            "response": response_data
        }, json_dumps_params={"indent": 4})
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

def chat_ui(request):
    return render(request, "chat/chat_ui.html")

def admin_portal(request):
    return render(request, "chat/admin_portal.html")

@csrf_exempt
def get_regex_rules(request):
    return JsonResponse({"rules": list(RegexRoutingPolicy.objects.values())})

@csrf_exempt
@require_POST
def add_regex_rule(request):
    try:
        data = json.loads(request.body)
        RegexRoutingPolicy.objects.create(**data)
        return JsonResponse({"message": "Rule added successfully!"}, status=201)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
def delete_regex_rule(request, rule_id):
    rule = get_object_or_404(RegexRoutingPolicy, id=rule_id)
    rule.delete()
    return JsonResponse({"message": "Rule deleted successfully!"})

@csrf_exempt
def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        file_name_parts = uploaded_file.name.rsplit('.', 1)
        file_type = file_name_parts[1].upper() if len(file_name_parts) > 1 else None

        if not file_type:
            return JsonResponse({"error": "Invalid file format."}, status=400)

        try:
            routing = FileUploadRouting.objects.get(file_type=file_type)
            return JsonResponse({
                "provider": routing.provider,
                "model": routing.model,
                "response": f"{routing.provider.capitalize()}: File processed successfully."
            })
        except FileUploadRouting.DoesNotExist:
            return JsonResponse({"error": f"No provider configured for {file_type} files."}, status=400)
    return JsonResponse({"error": "Invalid request."}, status=400)

@csrf_exempt
def get_file_types(request):
    return JsonResponse(list(FileUploadRouting.objects.values()), safe=False)

@csrf_exempt
@require_POST
def add_file_type(request):
    try:
        data = json.loads(request.body)
        FileUploadRouting.objects.create(**data)
        return JsonResponse({"message": "File type added successfully"}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

@csrf_exempt
def update_file_type(request, file_type_id):
    if request.method == "PUT":
        try:
            data = json.loads(request.body)
            file_type_config = get_object_or_404(FileUploadRouting, id=file_type_id)
            for field, value in data.items():
                setattr(file_type_config, field, value)
            file_type_config.save()
            return JsonResponse({"message": "File type updated successfully"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

@csrf_exempt
def delete_file_type(request, file_type_id):
    file_type_config = get_object_or_404(FileUploadRouting, id=file_type_id)
    file_type_config.delete()
    return JsonResponse({"message": "File type deleted successfully"})
