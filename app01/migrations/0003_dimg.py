# Generated by Django 3.2.5 on 2022-08-03 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='dImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_url', models.ImageField(upload_to='')),
            ],
        ),
    ]
