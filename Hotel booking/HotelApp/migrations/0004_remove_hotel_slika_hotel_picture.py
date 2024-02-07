# Generated by Django 4.2.1 on 2023-06-03 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HotelApp', '0003_hotel_slika'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='slika',
        ),
        migrations.AddField(
            model_name='hotel',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='hotel_pictures'),
        ),
    ]
