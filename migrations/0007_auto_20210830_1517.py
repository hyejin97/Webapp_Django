# Generated by Django 3.1.5 on 2021-08-30 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myenglishmate', '0006_auto_20210830_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expression',
            name='tags',
            field=models.ManyToManyField(blank=True, to='myenglishmate.Tag'),
        ),
    ]