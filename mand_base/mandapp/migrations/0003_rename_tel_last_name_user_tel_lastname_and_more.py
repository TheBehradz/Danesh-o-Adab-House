# Generated by Django 4.1 on 2023-12-06 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mandapp', '0002_user_completed_user_data_user_tel_firstname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='tel_last_name',
            new_name='tel_lastname',
        ),
        migrations.AlterField(
            model_name='user',
            name='major',
            field=models.IntegerField(blank=True, choices=[(0, 'ریاضی'), (1, 'تجربی'), (2, 'انسانی'), (3, 'هنر'), (4, 'سایر')], default=None, null=True),
        ),
    ]