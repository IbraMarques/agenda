# Generated by Django 3.0.6 on 2020-05-29 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_evento_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='local_evento',
            field=models.TextField(blank=True, null=True),
        ),
    ]