# Generated by Django 4.2.1 on 2023-11-03 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('placas', '0002_remove_solardata_tate_solardata_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solardata',
            old_name='sTATE',
            new_name='STATE',
        ),
    ]
