# Generated by Django 3.1.5 on 2021-02-01 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myenglishmate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expression',
            name='example',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='expression',
            name='explanation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='expression',
            name='tags',
            field=models.ManyToManyField(blank=True, to='myenglishmate.tag'),
        ),
    ]
