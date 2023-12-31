# Generated by Django 3.2.22 on 2023-10-26 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_direccion_user_rut'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tamano',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tamano', models.CharField(choices=[('pequeño', 'Pequeño'), ('mediano', 'Mediano'), ('grande', 'Grande')], max_length=10, unique=True)),
                ('descripcion', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='estacionamiento',
            name='complemento',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='estacionamiento',
            name='tamano',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.tamano'),
        ),
    ]
