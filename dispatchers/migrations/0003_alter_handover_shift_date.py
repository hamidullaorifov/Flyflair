# Generated by Django 5.2 on 2025-04-21 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dispatchers', '0002_remove_handover_aog_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='handover',
            name='shift_date',
            field=models.DateField(),
        ),
    ]
