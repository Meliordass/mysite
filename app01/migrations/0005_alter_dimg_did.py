# Generated by Django 3.2.5 on 2022-08-03 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20220803_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimg',
            name='did',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.img'),
        ),
    ]
