# Generated by Django 4.1.1 on 2023-01-13 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0006_alter_record_time_worked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='record',
            name='Time_worked',
            field=models.FloatField(blank=True, null=True, verbose_name='time-worked'),
        ),
    ]