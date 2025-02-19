# Generated by Django 5.1.6 on 2025-02-19 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_regexroutingrule'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUploadRoutingRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=50, unique=True)),
                ('provider', models.CharField(max_length=100)),
                ('model_name', models.CharField(max_length=100)),
            ],
        ),
    ]
