# Generated by Django 5.0.6 on 2024-06-22 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_verification', '0005_image_verification_lable_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image_verification',
            old_name='lable',
            new_name='label',
        ),
        migrations.AddField(
            model_name='image_verification',
            name='face_encoding',
            field=models.TextField(null=True),
        ),
    ]
