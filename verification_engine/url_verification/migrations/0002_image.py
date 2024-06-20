# Generated by Django 5.0.6 on 2024-06-20 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('url_verification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField(unique=True)),
                ('image_hash', models.CharField(max_length=255, unique=True)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
