# Generated by Django 3.2 on 2021-10-06 06:24

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0027_alter_new_high'),
    ]

    operations = [
        migrations.AddField(
            model_name='new',
            name='senior',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
        migrations.AlterField(
            model_name='new',
            name='high',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
    ]
