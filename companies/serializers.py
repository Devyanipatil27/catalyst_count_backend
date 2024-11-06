from rest_framework import serializers
from .models import CSVRecord


class CSVRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSVRecord
        fields = '__all__'  # You can specify individual fields if needed
