# Install Celery and Redis as a message broker

# tasks.py
from celery import shared_task
import pandas as pd
from .models import CSVRecord
import logging

logger = logging.getLogger(__name__)


@shared_task
def process_csv_file(file_path):
    try:
        data = pd.read_csv(file_path)
        logger.info(f"Processing CSV file. Number of rows: {len(data)}")

        records_to_create = []

        for _, row in data.iterrows():
            def safe_strip(value):
                if pd.isna(value):
                    return None
                return str(value).strip()

            record_data = CSVRecord(
                name=safe_strip(row.get('name')),
                domain=safe_strip(row.get('domain')) or 'unknown',
                year_founded=row.get('year founded') if pd.notna(
                    row.get('year founded')) else None,
                industry=safe_strip(row.get('industry')),
                size_range=safe_strip(row.get('size range')),
                locality=safe_strip(row.get('locality')),
                country=safe_strip(row.get('country')),
                linkedin_url=safe_strip(row.get('linkedin url')),
                current_employee_estimate=row.get('current employee estimate'),
                total_employee_estimate=row.get('total employee estimate'),
            )
            records_to_create.append(record_data)

        CSVRecord.objects.bulk_create(records_to_create)
        logger.info("CSV processing completed and records saved.")
    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
