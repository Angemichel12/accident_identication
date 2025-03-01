# Generated by Django 5.1.3 on 2025-03-01 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accident', '0003_alter_accident_latitude_alter_accident_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accident',
            name='latitude',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
        migrations.AlterField(
            model_name='accident',
            name='longitude',
            field=models.DecimalField(decimal_places=7, max_digits=10),
        ),
    ]
