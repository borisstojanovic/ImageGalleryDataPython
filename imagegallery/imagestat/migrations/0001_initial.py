# Generated by Django 3.1.5 on 2021-01-25 12:14

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=256)),
            ],
            options={
                'db_table': 'comment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=512, null=True)),
                ('path', cloudinary.models.CloudinaryField(blank=True, max_length=255)),
                ('time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'images',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
                ('session_id', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('expires', models.PositiveIntegerField()),
                ('data', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'sessions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=45)),
                ('password', models.CharField(max_length=256)),
                ('date_created', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
