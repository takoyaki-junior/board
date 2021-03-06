# Generated by Django 4.0.1 on 2022-03-15 13:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255, verbose_name='本文')),
                ('created_at', models.DateField(default=django.utils.timezone.now, verbose_name='作成日')),
            ],
            options={
                'db_table': 'topic',
            },
        ),
    ]
