# Generated by Django 5.1.7 on 2025-03-14 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "jobs",
            "0002_rename_jobs_job_categor_653d6e_idx_job_categor_55e998_idx_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="job",
            name="posted_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="jobapplication",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="jobbookmark",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
