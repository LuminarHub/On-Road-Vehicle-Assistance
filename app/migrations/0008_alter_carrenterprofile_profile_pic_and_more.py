# Generated by Django 5.0.2 on 2024-04-09 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_carreserve_ticket_code_alter_rentcar_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrenterprofile',
            name='profile_pic',
            field=models.ImageField(blank=True, default='static/images/profile/default.jpg', null=True, upload_to='pic_pics'),
        ),
        migrations.AlterField(
            model_name='rentcar',
            name='car_img',
            field=models.ImageField(blank=True, default='static/images/car/default.jpg', null=True, upload_to='car_pics'),
        ),
    ]