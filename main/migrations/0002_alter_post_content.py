# Generated by Django 4.1.7 on 2023-03-14 10:45

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]
