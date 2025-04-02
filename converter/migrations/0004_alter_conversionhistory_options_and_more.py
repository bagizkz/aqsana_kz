# Generated by Django 5.1.7 on 2025-04-02 05:48

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('converter', '0003_favoriteconversiondirection_delete_favoritecurrency'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversionhistory',
            options={'ordering': ['-created_at'], 'verbose_name': 'История конвертации', 'verbose_name_plural': 'История конвертаций'},
        ),
        migrations.AlterModelOptions(
            name='currency',
            options={'ordering': ['code'], 'verbose_name': 'Валюта', 'verbose_name_plural': 'Валюты'},
        ),
        migrations.AlterModelOptions(
            name='exchangerate',
            options={'ordering': ['-date'], 'verbose_name': 'Курс обмена', 'verbose_name_plural': 'Курсы обмена'},
        ),
        migrations.AlterModelOptions(
            name='favoriteconversiondirection',
            options={'ordering': ['user', 'from_currency__code', 'to_currency__code'], 'verbose_name': 'Избранное направление', 'verbose_name_plural': 'Избранные направления'},
        ),
        migrations.RemoveField(
            model_name='conversionhistory',
            name='timestamp',
        ),
        migrations.AddField(
            model_name='conversionhistory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Создано'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='conversionhistory',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Обновлено'),
        ),
        migrations.AlterField(
            model_name='conversionhistory',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='conversionhistory',
            name='converted_amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Сконвертировано'),
        ),
        migrations.AlterField(
            model_name='conversionhistory',
            name='from_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_from', to='converter.currency', verbose_name='Из валюты'),
        ),
        migrations.AlterField(
            model_name='conversionhistory',
            name='to_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_to', to='converter.currency', verbose_name='В валюту'),
        ),
        migrations.AlterField(
            model_name='conversionhistory',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='code',
            field=models.CharField(max_length=3, unique=True, verbose_name='Код валюты'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='currency',
            name='symbol',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Символ'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='base_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='base_rates', to='converter.currency', verbose_name='Базовая валюта'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='rate',
            field=models.DecimalField(decimal_places=6, max_digits=20, verbose_name='Курс'),
        ),
        migrations.AlterField(
            model_name='exchangerate',
            name='target_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_rates', to='converter.currency', verbose_name='Целевая валюта'),
        ),
        migrations.AlterField(
            model_name='favoriteconversiondirection',
            name='from_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_from', to='converter.currency', verbose_name='Из валюты'),
        ),
        migrations.AlterField(
            model_name='favoriteconversiondirection',
            name='to_currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_to', to='converter.currency', verbose_name='В валюту'),
        ),
        migrations.AlterField(
            model_name='favoriteconversiondirection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
    ]
