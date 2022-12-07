# Generated by Django 4.1.1 on 2022-12-07 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('five_s', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='holdinggrid',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='holdinggrid',
            name='criteria',
        ),
        migrations.RemoveField(
            model_name='holdinggrid',
            name='response',
        ),
        migrations.CreateModel(
            name='HoldingGridCriteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.BooleanField(default=False)),
                ('comment', models.CharField(blank=True, max_length=150, null=True)),
                ('criteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='five_s.criteria')),
                ('holding_grid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='five_s.holdinggrid')),
            ],
        ),
        migrations.AddField(
            model_name='holdinggrid',
            name='criterias',
            field=models.ManyToManyField(blank=True, through='five_s.HoldingGridCriteria', to='five_s.criteria'),
        ),
    ]
