from django.contrib import admin
from .models import FileRouting, RegexRoutingPolicy

class RegexRoutingPolicyAdmin(admin.ModelAdmin):
    list_display = ('regex_pattern', 'original_model', 'redirect_model')
    search_fields = ('regex_pattern', 'original_model', 'redirect_model')

admin.site.register(RegexRoutingPolicy, RegexRoutingPolicyAdmin)

@admin.register(FileRouting)
class FileRoutingAdmin(admin.ModelAdmin):
    list_display = ("file_type", "provider", "model")
    search_fields = ("file_type", "provider", "model")