from django.contrib import admin
from django.urls import path
from chat.views import (
    get_models, chat_ui, admin_portal, add_regex_rule, get_regex_rules,
    delete_regex_rule, chat_completions, upload_file, get_file_types,
    add_file_type, update_file_type, delete_file_type, sign_in, user_dashboard, admin_login
)

urlpatterns = [
    path('', sign_in, name='sign_in'),
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('admin/login/', admin_login, name='admin_login'),

    path('upload/', upload_file, name='upload_file'),
    path('chat/', chat_ui, name='chat_ui'),
    path('v1/chat/completions', chat_completions, name='chat_completions'),
    path('models/', get_models, name='get_models'),

    path("admin/add_regex_rule/", add_regex_rule, name="add_regex_rule"),
    path("admin/get_regex_rules/", get_regex_rules, name="get_regex_rules"),
    path("admin/delete_regex_rule/<int:rule_id>/", delete_regex_rule, name="delete_regex_rule"),

    path("admin/", admin_portal, name="admin_portal"),
    path("admin/file-types/", get_file_types, name="get_file_types"),
    path("admin/file-types/add/", add_file_type, name="add_file_type"),
    path("admin/file-types/<int:file_type_id>/update/", update_file_type, name="update_file_type"),
    path("admin/file-types/<int:file_type_id>/delete/", delete_file_type, name="delete_file_type"),
]
