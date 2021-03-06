# Generated by Django 3.2 on 2021-10-06 14:53

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0028_auto_20211006_1154'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='new',
            name='approved1',
        ),
        migrations.RemoveField(
            model_name='new',
            name='approved2',
        ),
        migrations.RemoveField(
            model_name='new',
            name='approved3',
        ),
        migrations.RemoveField(
            model_name='new',
            name='declined1',
        ),
        migrations.RemoveField(
            model_name='new',
            name='declined2',
        ),
        migrations.RemoveField(
            model_name='new',
            name='declined3',
        ),
        migrations.RemoveField(
            model_name='new',
            name='dlink',
        ),
        migrations.AddField(
            model_name='new',
            name='aadhar',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='new',
            name='college',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='new',
            name='graduation',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='new',
            name='masters',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='new',
            name='pan',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='new',
            name='phd',
            field=models.FileField(blank=True, default=None, null=True, upload_to=accounts.models.user_directory_path),
        ),
        migrations.AddField(
            model_name='new',
            name='status2',
            field=models.BooleanField(blank=True, choices=[(True, 'Approved'), (False, 'Declined')], default=None, null=True),
        ),
        migrations.AddField(
            model_name='new',
            name='status3',
            field=models.BooleanField(blank=True, choices=[(True, 'Approved'), (False, 'Declined')], default=None, null=True),
        ),
        migrations.AlterField(
            model_name='new',
            name='aadharn',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='new',
            name='email',
            field=models.EmailField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='new',
            name='pann',
            field=models.IntegerField(null=True),
        ),
    ]
