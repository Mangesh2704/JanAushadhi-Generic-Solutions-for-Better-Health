# Generated by Django 5.1.1 on 2024-09-22 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_remove_medicine_stock_alter_medicine_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='medicines/'),
        ),
    ]