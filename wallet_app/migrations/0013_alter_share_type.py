# Generated by Django 4.1 on 2023-01-09 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_app', '0012_share_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='type',
            field=models.CharField(choices=[('fiss', 'Fiis'), ('capital_shares', 'Ações')], default=None, max_length=50, verbose_name='Tipo de ação'),
        ),
    ]
