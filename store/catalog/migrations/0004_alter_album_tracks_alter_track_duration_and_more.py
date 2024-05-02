# Generated by Django 5.0.4 on 2024-05-02 00:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_remove_track_order"),
    ]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="tracks",
            field=models.ManyToManyField(
                blank=True, related_name="albums", to="catalog.track"
            ),
        ),
        migrations.AlterField(
            model_name="track",
            name="duration",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="track",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
