# Generated by Django 5.0.3 on 2024-07-15 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_alter_reqtomechanic_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='exp',
            field=models.CharField(max_length=100),
        ),
    ]
