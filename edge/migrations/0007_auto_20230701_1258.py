# Generated by Django 4.2.2 on 2023-07-01 09:58

from django.db import migrations,models


class Migration(migrations.Migration):

    dependencies = [
        ('edge', '0006_alter_booking_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='organizer_id',
            field=models.IntegerField(),
        ),
    ]