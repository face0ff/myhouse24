# Generated by Django 4.1.7 on 2023-04-13 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import house_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('services_app', '0005_item_requisite_meterreading'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('house_app', '0010_alter_invoice_services_alter_invoiceservice_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transfers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.BigIntegerField(default=house_app.models.transfer_number, unique=True, verbose_name='Номер ведомости')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Сумма')),
                ('completed', models.BooleanField(default=True, verbose_name='Проведен')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('income', models.BooleanField(default=True, verbose_name='Приходная ведомость')),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='house_app.account', verbose_name='Лицевой счет')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='services_app.item', verbose_name='Статья')),
                ('manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='manager', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='owner', to=settings.AUTH_USER_MODEL, verbose_name='Владелец квартиры')),
            ],
            options={
                'verbose_name': 'Приход/Расход',
                'verbose_name_plural': 'Приходные/Расходные ведомости',
            },
        ),
    ]