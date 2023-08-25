# Generated by Django 4.1.7 on 2023-08-25 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0012_post_thumbnail_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="thumbnail_url",
            field=models.URLField(
                blank=True,
                default="https://www.spectraresearch.com/wp-content/uploads/2022/09/default-image.jpg",
                null=True,
            ),
        ),
    ]