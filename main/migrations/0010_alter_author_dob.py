# Generated by Django 4.1.7 on 2023-07-08 19:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_alter_author_dob"),
    ]

    operations = [
        migrations.AlterField(
            model_name="author",
            name="dob",
            field=models.DateField(default=datetime.date(2023, 7, 9), null=True),
        ),
    ]
