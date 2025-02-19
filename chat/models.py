from django.db import models

# Create your models here.
class ModelProvider(models.Model):
    name=models.CharField(max_length=100,unique=True)
    provider=models.CharField(max_length=100)

    def __str__(self):
        return f"{self.provider}/{self.name}"

class RegexRoutingPolicy(models.Model):
    regex_pattern = models.CharField(max_length=255, unique=True)
    original_model = models.CharField(max_length=100)
    redirect_model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.regex_pattern} → {self.redirect_model}"

class FileUploadRouting(models.Model):
    file_type = models.CharField(max_length=50, unique=True)
    provider = models.CharField(max_length=50)
    model = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.file_type} -> {self.provider} ({self.model})"