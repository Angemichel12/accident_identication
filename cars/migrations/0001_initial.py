# Generated by Django 5.1.3 on 2025-01-01 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plate_number', models.CharField(max_length=8)),
                ('driver_name', models.CharField(max_length=50)),
                ('driver_phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('chassis_number', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
            ],
        ),
    ]
