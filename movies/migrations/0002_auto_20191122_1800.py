# Generated by Django 2.2.4 on 2019-11-22 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='backdrop_path',
            field=models.TextField(null=True),
        ),
    ]
