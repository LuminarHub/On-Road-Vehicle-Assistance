# Generated by Django 5.0 on 2024-10-22 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_userpayment_exp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rentcar',
            name='discription',
            field=models.TextField(),
        ),
    ]