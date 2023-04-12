# Generated by Django 4.1.7 on 2023-04-10 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services_app', '0005_item_requisite_meterreading'),
        ('house_app', '0009_invoice_alter_account_apartment_invoiceservice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='services',
            field=models.ManyToManyField(through='house_app.InvoiceService', to='services_app.services', verbose_name='Услуги'),
        ),
        migrations.AlterField(
            model_name='invoiceservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services_app.services', verbose_name='Услуга'),
        ),
    ]
