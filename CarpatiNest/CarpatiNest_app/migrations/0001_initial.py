# Generated by Django 5.2.1 on 2025-05-23 10:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mountain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nume munte')),
                ('description', models.TextField(verbose_name='Descriere')),
                ('altitude', models.IntegerField(verbose_name='Altitudine (m)')),
                ('image', models.ImageField(blank=True, null=True, upload_to='mountains/', verbose_name='Imagine')),
            ],
            options={
                'verbose_name': 'Munte',
                'verbose_name_plural': 'Munți',
            },
        ),
        migrations.CreateModel(
            name='Refuge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nume refugiu')),
                ('altitude', models.IntegerField(verbose_name='Altitudine (m)')),
                ('capacity', models.IntegerField(verbose_name='Capacitate')),
                ('description', models.TextField(verbose_name='Descriere')),
                ('location', models.CharField(max_length=200, verbose_name='Locație')),
                ('image', models.ImageField(blank=True, null=True, upload_to='refuges/', verbose_name='Imagine')),
                ('mountain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refuges', to='CarpatiNest_app.mountain', verbose_name='Munte')),
            ],
            options={
                'verbose_name': 'Refugiu',
                'verbose_name_plural': 'Refugii',
            },
        ),
    ]
