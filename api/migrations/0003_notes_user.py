# Generated by Django 5.1.5 on 2025-02-01 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_notes_updated_at_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='user',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='api.userprofile'),
            preserve_default=False,
        ),
    ]
