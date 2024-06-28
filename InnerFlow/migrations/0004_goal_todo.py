# Generated by Django 5.0.4 on 2024-06-28 11:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('InnerFlow', '0003_board_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('goal_id', models.AutoField(primary_key=True, serialize=False)),
                ('goal', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('todo_id', models.AutoField(primary_key=True, serialize=False)),
                ('todo', models.CharField(max_length=255)),
                ('checked', models.BooleanField(default=False)),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='InnerFlow.goal')),
            ],
        ),
    ]
