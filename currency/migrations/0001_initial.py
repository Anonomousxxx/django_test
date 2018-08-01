from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('currency_1',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchangerate_currency1', to='currency.Currency')),
                ('currency_2',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exchangerate_currency2', to='currency.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='UserExchangeRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reversed', models.BooleanField()),
                ('exchange_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currency.ExchangeRate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userexchangerate',
            unique_together={('user', 'exchange_rate', 'reversed')},
        ),
        migrations.AlterUniqueTogether(
            name='exchangerate',
            unique_together={('currency_1', 'currency_2')},
        ),
    ]
