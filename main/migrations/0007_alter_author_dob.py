# Generated by Django 4.1.7 on 2023-04-12 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_alter_author_dob"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="dob",
            field=models.DateField(default=datetime.date(2023, 4, 12)),
        ),
    ]