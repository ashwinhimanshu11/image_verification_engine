# Generated by Django 5.0.6 on 2024-06-20 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_verification', '0003_alter_image_verification_image_hash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image_verification',
            name='image_source',
            field=models.URLField(),
        ),
    ]
