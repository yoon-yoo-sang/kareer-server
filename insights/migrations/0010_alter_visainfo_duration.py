# Generated by Django 5.1.7 on 2025-04-16 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("insights", "0009_alter_cultureinfo_culture_type_industryinfo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="visainfo",
            name="duration",
            field=models.CharField(max_length=255),
        ),
    ]
