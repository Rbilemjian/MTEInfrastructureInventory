# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructureinventoryapp', '0002_auto_20180925_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applicationserver',
            name='network_info',
        ),
        migrations.RemoveField(
            model_name='applicationserver',
            name='storage_info',
        ),
        migrations.RemoveField(
            model_name='applicationserver',
            name='warranty_info',
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='base_warranty',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='c_drive',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='cpu',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='d_drive',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='dmz_public_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='e_drive',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='nat_ip_or_ilo',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='network',
            field=models.CharField(max_length=4, default='Corp', choices=[('Corp', 'Corp'), ('DMZ', 'DMZ')]),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='next_hardware_support_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='nic_mac_address',
            field=models.CharField(max_length=23, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='private_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='purchase_order',
            field=models.CharField(max_length=20, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='ram',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='storage_type',
            field=models.CharField(max_length=15, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='switch_or_port',
            field=models.CharField(max_length=40, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='virtual_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='NetworkInfo',
        ),
        migrations.DeleteModel(
            name='StorageInfo',
        ),
        migrations.DeleteModel(
            name='WarrantyInfo',
        ),
    ]
