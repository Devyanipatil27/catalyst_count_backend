# app_name/tasks.py

from celery import shared_task
import pandas as pd
import os
from .models import CSVRecord
from django.conf import settings


@shared_task
def process_csv_file(file_path):
    try:
        chunk_size = 10000  # Process 10,000 rows at a time
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            for index, row in chunk.iterrows():
                record_data = {
                    'domain': row.get('domain', '').strip(),
                    'year_founded': row.get('year founded'),
                    'industry': row.get('industry', '').strip(),
                    'size_range': row.get('size range', '').strip(),
                    'locality': row.get('locality', '').strip(),
                    'country': row.get('country', '').strip(),
                    'linkedin_url': row.get('linkedin url', '').strip(),
                    'current_employee_estimate': row.get('current employee estimate'),
                    'total_employee_estimate': row.get('total employee estimate'),
                }

                obj, created = CSVRecord.objects.update_or_create(
                    name=row['name'].strip(),
                    defaults=record_data,
                )
    except Exception as e:
        print(f"Error processing CSV: {e}")
