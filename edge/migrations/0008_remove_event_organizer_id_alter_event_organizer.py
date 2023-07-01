# Generated by Django 4.2.2 on 2023-07-01 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('edge', '0007_auto_20230701_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='organizer_id',
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(default='Unknown', on_delete=django.db.models.deletion.CASCADE, related_name='organized_events', to=settings.AUTH_USER_MODEL),
        ),
    ]