# Generated by Django 5.1.7 on 2025-03-27 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levelupapp', '0002_score_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='score',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
