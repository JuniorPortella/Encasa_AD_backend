# Generated by Django 4.2.1 on 2023-09-04 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orcamento', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='bairro',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='cidade',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='rua',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
