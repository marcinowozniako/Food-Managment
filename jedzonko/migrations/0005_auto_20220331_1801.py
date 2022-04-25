# Generated by Django 2.2.6 on 2022-03-31 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jedzonko', '0004_auto_20220331_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeplan',
            name='day_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.DayName'),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Plan'),
        ),
        migrations.AlterField(
            model_name='recipeplan',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jedzonko.Recipe'),
        ),
    ]