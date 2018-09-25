# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructureinventoryapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationserver',
            name='network_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='infrastructureinventoryapp.NetworkInfo'),
        ),
        migrations.AlterField(
            model_name='applicationserver',
            name='storage_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='infrastructureinventoryapp.StorageInfo'),
        ),
        migrations.AlterField(
            model_name='applicationserver',
            name='warranty_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='infrastructureinventoryapp.WarrantyInfo'),
        ),
    ]
