# Generated by Django 3.2.23 on 2023-11-22 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_rename_fecha_arrendamiento_fecha_inicion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='arrendamiento',
            old_name='fecha_inicion',
            new_name='fecha_inicio',
        ),
    ]