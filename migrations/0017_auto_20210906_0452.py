# Generated by Django 3.1.5 on 2021-09-06 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myenglishmate', '0016_auto_20210906_0430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expression',
            name='tags',
        ),
        migrations.DeleteModel(
            name='tag',
        ),
    ]
