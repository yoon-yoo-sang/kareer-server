# Generated by Django 5.1.7 on 2025-03-14 04:26

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="authuser",
            name="created_at",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="authuser",
            name="deleted_at",
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name="authuser",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddIndex(
            model_name="authuser",
            index=models.Index(
                fields=["created_at"], name="authenticat_created_319d30_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="authuser",
            index=models.Index(
                fields=["updated_at"], name="authenticat_updated_3984dc_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="authuser",
            index=models.Index(
                fields=["deleted_at"], name="authenticat_deleted_964f46_idx"
            ),
        ),
    ]
