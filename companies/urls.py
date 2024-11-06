from django.urls import path
from .views import RegisterView, LoginView, DashboardView, LogoutView, UploadCSVView, QueryBuilderView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),  # Redirect to login page
    path('register/', RegisterView.as_view(), name='register'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload_csv/', UploadCSVView.as_view(), name='upload_csv'),
    path('query_builder/', QueryBuilderView.as_view(), name='query_builder'),
]
