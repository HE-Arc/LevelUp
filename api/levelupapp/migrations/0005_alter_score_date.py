# Generated by Django 5.1.7 on 2025-03-27 10:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapp', '0004_alter_score_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='date',
            field=models.DateTimeField(default=models.DateTimeField(default=django.utils.timezone.now)),
        ),
    ]
