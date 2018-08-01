from django.db import migrations

init_currencies = ['USD', 'BTC']


# initially save usd and btc to db
def create_initial_currencies(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    currency = apps.get_model("currency", "Currency")
    for name in init_currencies:
        currency.objects.using(db_alias).create(name=name)


class Migration(migrations.Migration):
    dependencies = [
        ('currency', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_currencies),
    ]
