# Generated by Django 5.1.7 on 2025-03-14 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "authentication",
            "0003_remove_authuser_authenticat_created_319d30_idx_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="authuser",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
