# Generated by Django 3.2.22 on 2023-10-26 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20231026_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrendamiento',
            name='fecha_fin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='arrendamiento',
            name='fecha_inicio',
            field=models.DateTimeField(),
        ),
    ]
