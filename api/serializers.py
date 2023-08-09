from .models import Employee
from rest_framework import serializers
from . models import Company, Employee


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

# Custom Serializer


class WorksAtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'location', 'employee_size')


class EmployeeSerializer(serializers.ModelSerializer):
    works_at = WorksAtSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

# Override relational data retrieve
    def to_representation(self, instance):
        data = super().to_representation(instance)

        include_works_at = self.context.get('include_works_at', False)
        if not include_works_at:
            data['works_at'] = data['works_at']['id']

        return data

    def validate_works_at(self, value):
        if self.partial:
            return value

        if not (Company.objects.get(pk=value)):
            raise serializers.ValidationError("Invalid company ID")
        return value

    def validate(self, data):
        if self.partial:
            return data

        errors = {}

        first_name = data.get('first_name')
        if len(first_name) < 2:
            errors['first_name'] = "At least 2 characters long."

        last_name = data.get('last_name')
        if len(last_name) < 2:
            errors['last_name'] = "At least 2 characters long."

        dob = data.get('dob')
        from datetime import date
        if dob and dob > date.today():
            errors['dob'] = "Date of birth cannot be in the future."

        gender = data.get('gender')
        if gender not in dict(Employee.GENDER_CHOICES):
            errors['gender'] = "Invalid gender choice."

        if errors:
            raise serializers.ValidationError(errors)

        return data
