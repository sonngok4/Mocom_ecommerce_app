# Generated by Django 5.0.4 on 2024-05-05 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['created_at'], name='product_pro_created_57e07a_idx'),
        ),
    ]
