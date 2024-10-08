# Generated by Django 5.0.6 on 2024-09-17 04:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customtest', '0002_tests_question_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_id', models.TextField(verbose_name='Fayl id')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customtest.tests', verbose_name='Test Nomi')),
            ],
            options={
                'verbose_name': 'Test Fayl',
                'verbose_name_plural': 'Test Fayllari',
            },
        ),
    ]
