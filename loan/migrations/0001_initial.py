# Generated by Django 4.1.7 on 2023-04-08 20:45

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
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=500, max_digits=10)),
                ('interest_rate', models.DecimalField(decimal_places=2, default=10, max_digits=4)),
                ('term', models.IntegerField(default=12)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('remaining_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('created_loan', models.DateTimeField(auto_now=True)),
                ('updated_loan', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('active', 'Active'), ('paid', 'Paid'), ('defaulted', 'Defaulted')], default='active', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-updated_loan', '-created_loan'],
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_type', models.CharField(choices=[('credit', 'Credit'), ('debit', 'Debit')], max_length=20)),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_mode', models.CharField(choices=[('UPI', 'UPI'), ('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('Debit Card', 'Debit Card'), ('Net Banking', 'Net Banking')], default='UPI', max_length=20)),
                ('payment_id', models.CharField(default='', max_length=50)),
                ('transaction_time', models.DateTimeField(auto_now=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loan.loan')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(default='', max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('dob', models.DateField(default='2000-01-01')),
                ('created', models.DateField(auto_now=True)),
                ('updated', models.DateField(auto_now_add=True)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoanRepayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('loan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repayments', to='loan.loan')),
            ],
        ),
    ]
