# Generated by Django 4.1.1 on 2022-10-13 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='Default User', max_length=50)),
                ('updated_by', models.CharField(default='Default User', max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=50, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('restored_by', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(default='Item name', max_length=100)),
                ('description', models.TextField(default='Item description')),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='Default User', max_length=50)),
                ('updated_by', models.CharField(default='Default User', max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=50, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('restored_by', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(default='Theme name', max_length=100)),
                ('description', models.TextField(default='Theme description')),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vmq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.CharField(default='Default User', max_length=50)),
                ('updated_by', models.CharField(default='Default User', max_length=50)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_by', models.CharField(blank=True, max_length=50, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('restored_by', models.CharField(blank=True, max_length=50, null=True)),
                ('reference', models.CharField(default='REF', max_length=100)),
                ('visit_date', models.DateField(default=django.utils.timezone.now)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.employee')),
            ],
            options={
                'ordering': ['-updated_at', '-created_at'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VmqItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('Conforme', 'Conforme'), ('Non Conforme', 'Non Conforme')], max_length=30)),
                ('type', models.CharField(choices=[('Application', 'Application'), ('Disposition', 'Disposition')], max_length=30)),
                ('comment', models.TextField(blank=True, null=True)),
                ('action', models.TextField(blank=True, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmq.item')),
                ('vmq', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmq.vmq')),
            ],
        ),
        migrations.AddField(
            model_name='vmq',
            name='items',
            field=models.ManyToManyField(blank=True, through='vmq.VmqItem', to='vmq.item'),
        ),
        migrations.AddField(
            model_name='vmq',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vmq',
            name='workshop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.workshop'),
        ),
        migrations.AddField(
            model_name='item',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmq.theme'),
        ),
    ]
