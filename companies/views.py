from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import UploadCSVForm  # Assuming you have a form for CSV upload
import pandas as pd
from .models import CSVRecord
from django.contrib import messages
import logging


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid credentials'})


class DashboardView(View):
    def get(self, request):
        return render(request, 'dashboard.html', {'user': request.user})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class UploadCSVView(View):
    def post(self, request):
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            try:
                data = pd.read_csv(csv_file)
                print("CSV file successfully read. Number of rows:", len(data))

                records_to_create = []

                for index, row in data.iterrows():
                    # Safely strip values and handle NaNs by setting defaults
                    def safe_strip(value):
                        if pd.isna(value):
                            return None  # Use None if value is missing to handle nullable fields
                        return str(value).strip()

                    # Create record with default handling for missing fields
                    record_data = CSVRecord(
                        name=safe_strip(row.get('name')),
                        # Default to 'unknown' if domain is missing
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
                        total_employee_estimate=row.get(
                            'total employee estimate'),
                    )
                    records_to_create.append(record_data)
                    print(
                        f"Prepared record for {safe_strip(row.get('name')) or 'Unnamed Company'}")

                # Use bulk_create to add records
                CSVRecord.objects.bulk_create(records_to_create)
                print(f"Bulk created {len(records_to_create)} records.")

                return render(request, 'upload_csv.html', {
                    'form': form,
                    'success_message': 'CSV file processed successfully!'
                })

            except Exception as ex:
                print(f"An error occurred while processing the CSV file: {ex}")
                return render(request, 'upload_csv.html', {
                    'form': form,
                    'error_message': 'An error occurred while processing the CSV file.'
                })
        else:
            return render(request, 'upload_csv.html', {'form': form})


class QueryBuilderView(View):
    def get(self, request):
        return render(request, 'query_builder.html')

    def post(self, request):
        keyword = request.POST.get('keyword', '').strip()
        industry = request.POST.get('industry', '').strip()
        year_founded = request.POST.get('year_founded', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        country = request.POST.get('country', '').strip()
        employees_from = request.POST.get('employees_from', '').strip()
        employees_to = request.POST.get('employees_to', '').strip()
        size_range = request.POST.get('size_range', '').strip()

        queryset = CSVRecord.objects.filter()

        # Filtering based on user input
        if keyword:
            queryset = queryset.filter(name__icontains=keyword)

        if industry:
            queryset = queryset.filter(industry__icontains=industry)

        if year_founded:
            queryset = queryset.filter(year_founded=year_founded)

        if city:
            queryset = queryset.filter(locality__icontains=city)

        if state:
            queryset = queryset.filter(state__icontains=state)

        if country:
            queryset = queryset.filter(country__icontains=country)

        if employees_from:
            queryset = queryset.filter(
                total_employee_estimate__gte=employees_from)

        if employees_to:
            queryset = queryset.filter(
                total_employee_estimate__lte=employees_to)

        if size_range:
            queryset = queryset.filter(size_range__icontains=size_range)

        records = queryset

        # Success message
        messages.success(
            request, f'{records.count()} records found for the query')

        return render(request, 'query_builder.html', {'records': records})
