# Generated by Django 4.1.1 on 2023-01-13 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0008_alter_leave_no_of_days_alter_leave_pending_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave',
            name='Pending_Status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=25, null=True),
        ),
    ]
