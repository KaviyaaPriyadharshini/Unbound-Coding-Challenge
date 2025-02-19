from chat.models import FileRouting

FileRouting.objects.create(file_type="pdf", provider="anthropic", model="claude-v1")
FileRouting.objects.create(file_type="docx", provider="openai", model="gpt-4")

print(FileRouting.objects.all())  # Verify the records
