# Generated by Django 4.2.5 on 2023-11-21 05:31

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.RenameField(
            model_name='employeemodel',
            old_name='employeeId',
            new_name='employee_id',
        ),
        migrations.RenameField(
            model_name='employeemodel',
            old_name='employeeName',
            new_name='employee_name',
        ),
        migrations.RenameField(
            model_name='employeemodel',
            old_name='martialStatus',
            new_name='martial_status',
        ),
        migrations.RemoveField(
            model_name='employeemodel',
            name='dateOfBirth',
        ),
        migrations.AddField(
            model_name='employeemodel',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='employeemodel',
            name='employee_date_of_join',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='employeemodel',
            name='employee_phone',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employeemodel',
            name='employee_position',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employeemodel',
            name='employee_role',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='employeemodel',
            name='experience',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='LeavesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_annual_leaves', models.IntegerField()),
                ('leaves_consumed', models.IntegerField()),
                ('total_sick_leaves', models.IntegerField()),
                ('sick_leaves_consumed', models.IntegerField()),
                ('total_casual_leaves', models.IntegerField(default=24)),
                ('casual_leaves_consumed', models.IntegerField(default=0)),
                ('unpaid_leaves_consumed', models.IntegerField(default=0)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.employeemodel')),
            ],
        ),
        migrations.CreateModel(
            name='LeavesHistoryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField(default=django.utils.timezone.now)),
                ('to_date', models.DateField(default=django.utils.timezone.now)),
                ('number_of_days', models.IntegerField()),
                ('approved_by', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('leave_type', models.CharField(max_length=255)),
                ('reason', models.TextField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.employeemodel')),
                ('notify', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='leave_notifications', to='login.employeemodel')),
            ],
        ),
    ]
