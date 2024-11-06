from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from .forms import UploadCSVForm  # Assuming you have a form for CSV upload
import pandas as pd
from .models import CSVRecord
from django.contrib import messages


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
    def get(self, request):
        form = UploadCSVForm()
        return render(request, 'upload_csv.html', {'form': form})

    def post(self, request):
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            file_path = os.path.join(
                settings.MEDIA_ROOT, 'company_data', csv_file.name)

            # Create the 'company_data' directory if it doesn't exist
            os.makedirs(os.path.join(settings.MEDIA_ROOT,
                        'company_data'), exist_ok=True)

            with open(file_path, 'wb+') as destination:
                for chunk in csv_file.chunks():
                    destination.write(chunk)

            try:
                # Use pandas to read the CSV in chunks
                chunk_size = 10000  # Process 10,000 rows at a time
                for chunk in pd.read_csv(file_path, chunksize=chunk_size):
                    # Process each row in the chunk
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

                        # Use update_or_create to either update or create the record
                        obj, created = CSVRecord.objects.update_or_create(
                            name=row['name'].strip(),
                            defaults=record_data,
                        )

                return render(request, 'upload_csv.html', {
                    'form': form,
                    'success_message': 'CSV file processed successfully!'
                })

            except Exception as ex:
                print(ex)
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
            queryset = queryset.filter(name__icontains=industry)

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
