# Generated by Django 4.1.7 on 2023-04-03 07:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stream', '0002_warranty'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('transfer_status', models.CharField(choices=[('A', 'Approved'), ('P', 'Pending'), ('D', 'Denied')], default='P', max_length=1)),
                ('last_confirm', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stream.device')),
                ('transferee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transferees', to=settings.AUTH_USER_MODEL)),
                ('transferor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transferors', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]