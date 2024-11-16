# Generated by Django 5.1.3 on 2024-11-16 04:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Applied', 'Applied'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Hired', 'Hired')], default='Applied', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='core.jobpost')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='user_auth.jobseeker')),
            ],
        ),
    ]
