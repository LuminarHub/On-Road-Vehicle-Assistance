# Generated by Django 5.0.1 on 2024-06-27 04:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_userpayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpayment',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cust_pay', to='app.userprofile'),
        ),
        migrations.AlterField(
            model_name='userpayment',
            name='mechanic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mech_pay', to='app.mechanicprofile'),
        ),
        migrations.AlterField(
            model_name='userpayment',
            name='req',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pay', to='app.reqtomechanic'),
        ),
    ]
