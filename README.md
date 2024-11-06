# Catalyst Count

Catalyst Count is a web application built with Django, designed to upload, process, and store company data from CSV files. This project allows users to upload CSV files containing company information, and it processes and stores the data in a PostgreSQL database. The data includes company details such as domain, year founded, industry, size range, locality, country, LinkedIn URL, employee estimates, and more.

## Features

- **File Upload**: Upload CSV files containing company data.
- **Data Processing**: Processes large CSV files efficiently using pandas, with chunking to handle large datasets (up to 1 GB).
- **Database Storage**: Store company data in a PostgreSQL database, using Django ORM for efficient database management.
- **Data Validation**: Automatically validates and updates or creates records in the database.
- **User Interface**: A simple web interface to upload files and get feedback on the process.

## Installation

### Prerequisites
Before starting, make sure you have the following installed on your machine:
- Python 3.8 or higher
- PostgreSQL
- Django
- pip (Python package manager)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Devyanipatil27/catalyst_count_backend.git
   cd catalyst_count

2. **Createvirtualenv**:   
   python -m venv venv
   venv\Scripts\activate  # On Windows

3. **Install dependencies:**:
   pip install -r requirements.txt

4. **Set up the PostgreSQL database:**:
   DATABASE_URL=postgresql://catalyst_count_db:catalyst_count_db@localhost:5432/catalyst_count_db

5. **Run migrations:**:
   python manage.py migrate

6. **Create a superuser to access the Django admin:**:
   python manage.py createsuperuser

7. **Run the development server::**:
   python manage.py runserver

8. **Access the application::**:
   Open a web browser and go to http://127.0.0.1:8000 to access the app.