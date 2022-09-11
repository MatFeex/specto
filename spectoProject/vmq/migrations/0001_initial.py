# Generated by Django 4.1 on 2022-09-10 13:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuration', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('name', models.CharField(default='Item name', max_length=30)),
                ('description', models.TextField(default='Item description')),
            ],
            options={
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
                ('name', models.CharField(default='Theme name', max_length=30)),
                ('description', models.TextField(default='Theme description')),
            ],
            options={
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
                ('employee', models.IntegerField(default=1)),
                ('result', models.CharField(choices=[('Conforme', 'Conforme'), ('Non Conforme', 'Non Conforme')], default=('Conforme', 'Conforme'), max_length=30)),
                ('type', models.CharField(choices=[('Application', 'Application'), ('Disposition', 'Disposition')], default=('Application', 'Application'), max_length=30)),
                ('comment', models.TextField(default='Comment')),
                ('items', models.ManyToManyField(to='vmq.item')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workshop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuration.workshop')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='item',
            name='theme',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vmq.theme'),
        ),
    ]
