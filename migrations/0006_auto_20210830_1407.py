# Generated by Django 3.1.5 on 2021-08-30 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myenglishmate', '0005_auto_20210830_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expression',
            name='tags',
            field=models.ManyToManyField(blank=True, to='myenglishmate.Tag'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tagname',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
