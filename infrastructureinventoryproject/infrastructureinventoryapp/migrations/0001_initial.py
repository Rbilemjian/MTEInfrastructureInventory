# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('server_function', models.CharField(max_length=40)),
                ('hostname', models.CharField(max_length=30)),
                ('primary_application_function', models.CharField(max_length=40)),
                ('is_virtual_machine', models.BooleanField(default=False)),
                ('environment', models.CharField(max_length=4, choices=[('Prod', 'Production'), ('Dev', 'Development'), ('QA', 'Quality Assurance')])),
                ('location', models.CharField(max_length=40)),
                ('data_center', models.CharField(max_length=30)),
                ('rack', models.CharField(max_length=20, blank=True, null=True)),
                ('operating_system', models.CharField(max_length=30, blank=True)),
                ('model', models.CharField(max_length=30, blank=True, null=True)),
                ('serial_number', models.CharField(max_length=30, blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('network', models.CharField(max_length=4, choices=[('Corp', 'Corp'), ('DMZ', 'DMZ')])),
                ('private_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('dmz_public_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('virtual_ip', models.GenericIPAddressField(blank=True, null=True)),
                ('nat_ip_or_ilo', models.GenericIPAddressField(blank=True, null=True)),
                ('nic_mac_address', models.CharField(max_length=23, blank=True, null=True)),
                ('switch_or_port', models.CharField(max_length=40, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StorageInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('cpu', models.IntegerField(blank=True, null=True)),
                ('ram', models.IntegerField(blank=True, null=True)),
                ('c_drive', models.IntegerField(blank=True, null=True)),
                ('d_drive', models.IntegerField(blank=True, null=True)),
                ('e_drive', models.IntegerField(blank=True, null=True)),
                ('storage_type', models.CharField(max_length=15, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='WarrantyInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('purchase_order', models.CharField(max_length=20, blank=True, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('next_hardware_support_date', models.DateField(blank=True, null=True)),
                ('base_warranty', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='network_info',
            field=models.ForeignKey(to='infrastructureinventoryapp.NetworkInfo'),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='storage_info',
            field=models.ForeignKey(to='infrastructureinventoryapp.StorageInfo'),
        ),
        migrations.AddField(
            model_name='applicationserver',
            name='warranty_info',
            field=models.ForeignKey(to='infrastructureinventoryapp.WarrantyInfo'),
        ),
    ]
