# Generated by Django 4.1 on 2023-12-17 16:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mandapp', '0004_file_vrifcode_user_register_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='added_by',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='added_files', to='mandapp.user'),
        ),
    ]
