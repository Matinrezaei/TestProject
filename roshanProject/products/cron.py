import csv
from datetime import datetime
from .models import Product
from django.conf import settings
import os

def generate_csv_job():
    output_dir = settings.CSV_OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    file_name = f"top_three_products_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.csv"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, mode='w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['دسته‌بندی', 'نام محصول', 'تعداد بازدید'])

        products = Product.objects.order_by('-views')[:3]
        for product in products:
            writer.writerow([product.category.name, product.name, product.views])

    print(f"CSV file created at {file_path}")

