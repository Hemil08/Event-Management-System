# Generated by Django 5.1.2 on 2025-01-27 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_app', '0004_alter_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('Standup Comedy Shows', 'Standup Comedy Shows'), ('Music Concerts', 'Music Concerts'), ('Festivals', 'Festivals'), ('Party', 'Party')], default='standup_comedy_shows', max_length=20),
        ),
    ]
