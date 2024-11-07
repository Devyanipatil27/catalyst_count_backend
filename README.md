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
   
   createdb catalyst_count_db
   DB_NAME=catalyst_count_db
   DB_USER=catalyst_count_db
   DB_PASSWORD=catalyst_count_db
   DB_HOST=localhost
   DB_PORT=5432
   # Create the user
   psql -c "CREATE USER your-db-user WITH PASSWORD 'your-db-password';"
   psql -c "ALTER USER your-db-user CREATEDB;"

   # Grant permissions
   psql -c "GRANT ALL PRIVILEGES ON DATABASE catalyst_count_db TO your-db-user;"
   

5. **Run migrations:**:
   python manage.py migrate

6. **Create a superuser to access the Django admin:**:
   python manage.py createsuperuser

7. **Run the development server::**:
   python manage.py runserver

8. **Access the application::**:
   Open a web browser and go to http://127.0.0.1:8000 to access the app.

## Features and Functionality

### 1. **User Authentication**
- **User Registration**: The application allows users to register by creating an account with their username, email, and password. The registration form ensures that users provide valid details and checks for duplicate accounts.
- **Login and Logout**: Once registered, users can log in to their account using their credentials. Upon successful login, users can access the application’s core features, including data upload and querying. Users can also log out to terminate their session and ensure security.
- **Access Control**: Only authenticated users can interact with the features of the application. If a user is not logged in, they will be redirected to the login page when trying to access restricted pages such as the data upload and query builder pages.

### 2. **Data Upload and Management**
- **File Upload**: The application provides a simple and intuitive interface for users to upload CSV files containing company data. Users can select and upload CSV files of up to 1GB in size, which the system handles efficiently.
- **Data Validation**: Once a file is uploaded, the system automatically performs data validation to ensure the CSV file meets the required format. Any issues with the file are highlighted, allowing users to correct errors before the data is processed.
- **Data Processing in the Background**: The application processes uploaded CSV files asynchronously in the background to prevent blocking the request-response cycle. This ensures that users can continue interacting with the app while the data is being processed and stored.
- **Database Storage**: Once validated, the processed data is stored in a PostgreSQL database using Django’s ORM. This allows for efficient querying and manipulation of the data within the app.

### 3. **Query Builder**
- **Filterable Interface**: The query builder allows users to filter the uploaded company data based on various criteria such as industry, size, location, and more. Users can select different filters from dropdown menus or input fields to specify their search parameters.
- **Display Record Count**: After applying filters, the application displays the count of records that match the user's criteria, providing users with quick insights into the filtered data.
- **Dynamic Querying**: The query builder dynamically updates the displayed results based on the selected filters, providing an interactive and responsive user experience.

### 4. **Background Processing**
- **Handling Large Files**: To support large file uploads (up to 1GB), the application uses efficient background processing. When a file is uploaded, it is processed in chunks, and the data is imported into the database without impacting the responsiveness of the web interface.
- **Asynchronous Processing**: The application uses background task queues (such as Celery or Django Q) to handle data processing asynchronously. This ensures that even if the file size is large, the user is not forced to wait for the process to complete before continuing to use the app.
- **Progress Feedback**: While the file is being processed, users receive real-time progress updates, such as a progress bar or status message, to let them know how much of the file has been processed and when it will be completed.

### 5. **User Interface**
- **Responsive Design**: The application is designed with a clean, user-friendly interface using Bootstrap 4. It ensures that the application is responsive, meaning it adjusts seamlessly to different screen sizes and devices, such as desktops, tablets, and smartphones.
- **Login Page**: The login page provides a secure login form for users to access the app. It also includes options for password recovery and user registration for new users.
- **File Upload Page**: The file upload page allows users to select and upload CSV files. It includes drag-and-drop functionality as well as a standard file selection input for added convenience.
- **Query Builder Page**: The query builder page provides a flexible interface where users can filter and search through the uploaded data. It includes various input fields and dropdowns for customizing the search criteria.
- **Progress Indicators**: The user interface includes progress indicators (e.g., progress bars) to show users the status of the data upload and processing tasks, improving user experience and reducing wait-time frustration.

---

### Summary
The **Catalyst Count** web application combines several essential features for users to efficiently manage and interact with large datasets. It provides robust authentication, an easy-to-use data upload mechanism, powerful query filtering capabilities, and seamless background processing for handling large CSV files. The user interface is intuitive and responsive, ensuring a smooth experience across various devices. These features make Catalyst Count a valuable tool for managing company data at scale while maintaining high performance and usability.


## Docker Setup (Optional)

If you'd like to containerize the **Catalyst Count** application using Docker, follow the steps below to set up and run the application within Docker containers.

### 1. Dockerize the Application

First, ensure that you have Docker and Docker Compose installed on your machine. Then, follow these steps to containerize the application.

#### Build and Start the Containers:

To build the Docker images and start the containers, run the following command from the root directory of the project:

```bash
docker-compose up --build
