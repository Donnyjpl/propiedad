# Generated by Django 5.0.7 on 2024-07-24 20:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("web", "0002_alter_propiedad_tipo_propiedad"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="direccion",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="web.direccion",
            ),
        ),
    ]
