# Generated by Django 5.1.6 on 2025-02-19 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_modelprovider_provider'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegexRoutingRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_model', models.CharField(max_length=100)),
                ('regex_pattern', models.CharField(max_length=255)),
                ('redirect_model', models.CharField(max_length=100)),
            ],
        ),
    ]
