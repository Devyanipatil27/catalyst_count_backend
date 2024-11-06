from celery import shared_task
import pandas as pd
from .models import CSVRecord
import os


@shared_task
def process_csv_and_create_records(csv_file_path):
    try:
        # Read the CSV file asynchronously
        with open(csv_file_path, 'r') as file:
            data = pd.read_csv(file)
            records_to_create = []

            for index, row in data.iterrows():
                # Define safe strip function to handle missing values
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
                    current_employee_estimate=row.get(
                        'current employee estimate'),
                    total_employee_estimate=row.get('total employee estimate'),
                )
                records_to_create.append(record_data)

            # Bulk insert records into the database
            CSVRecord.objects.bulk_create(records_to_create)

        # Clean up the temporary file
        os.remove(csv_file_path)
        print(
            f"Successfully processed and created {len(records_to_create)} records.")
    except Exception as ex:
        print(f"Error occurred while processing the CSV file: {ex}")
