# Generated by Django 3.2.9 on 2021-11-02 19:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['seq']},
        ),
    ]