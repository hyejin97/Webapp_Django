# Generated by Django 3.1.5 on 2021-08-30 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myenglishmate', '0003_auto_20210824_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expression',
            name='tags',
            field=models.ManyToManyField(blank=True, to='myenglishmate.Tag'),
        ),
        migrations.AlterField(
            model_name='expression',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
