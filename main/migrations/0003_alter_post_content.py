# Generated by Django 4.1.7 on 2023-03-14 11:37

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_alter_post_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="content",
            field=tinymce.models.HTMLField(blank=True, null=True),
        ),
    ]
