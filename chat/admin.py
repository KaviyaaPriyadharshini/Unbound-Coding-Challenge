from django.contrib import admin
from .models import RegexRoutingPolicy, FileUploadRouting

class RegexRoutingPolicyAdmin(admin.ModelAdmin):
    list_display = ('regex_pattern', 'original_model', 'redirect_model')
    search_fields = ('regex_pattern', 'original_model', 'redirect_model')

admin.site.register(RegexRoutingPolicy, RegexRoutingPolicyAdmin)

@admin.register(FileUploadRouting)
class FileUploadRoutingAdmin(admin.ModelAdmin):
    list_display = ('file_type', 'provider', 'model')
    search_fields = ('file_type',)