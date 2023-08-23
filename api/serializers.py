from rest_framework import serializers
from datetime import timedelta, date
from . models import Company, Employee, Gear, GearLog


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):

    works_at = CompanySerializer(read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        include_company_details = self.context.get(
            'include_company_details', False)
        if not include_company_details:
            # Remove nested works_at field if not required
            representation['works_at'] = representation['works_at']['name']
        return representation


class EmployeeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'

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


class GearSerializer(serializers.ModelSerializer):
    owner = CompanySerializer(read_only=True)

    class Meta:
        model = Gear
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        include_owner_details = self.context.get(
            'include_owner_details', False)
        if not include_owner_details:
            # Remove nested owner field if not required
            representation['owner'] = representation['owner']['name']
        return representation


class GearCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gear
        fields = '__all__'

    def validate(self, data):
        if self.partial:
            return data

        errors = {}
        name = data.get('name')
        if len(name) < 2:
            errors['name'] = "At least 2 characters long."

        gear_type = data.get('gear_type')
        if len(gear_type) < 2:
            errors['gear_type'] = "At least 2 characters long."

        if errors:
            raise serializers.ValidationError(errors)

        return data


class GearLogSerializer(serializers.ModelSerializer):
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = GearLog
        fields = '__all__'

    def get_remaining_days(self, obj):
        current_date = date.today()
        remaining_days = (obj.checkout_date +
                          timedelta(days=obj.period)) - current_date
        return remaining_days.days if remaining_days.days > 0 else 0

    def validate(self, data):
        if self.partial:
            return data

        # raise validation error if a gear is already assigned to an employee
        # preventing a gear log entry
        existing_gear_log = GearLog.objects.filter(
            device=data['device'].id, returned=False)
        if existing_gear_log.exists():
            raise serializers.ValidationError(
                "This gear is already assigned to another employee.")

        # raise validation error if a gear isn't own by a company

        have_owner = Gear.objects.filter(
            id=data['device'].id, owner=data['company'].id)
        if not have_owner.exists():
            raise serializers.ValidationError(
                "Invalid gear ID or not owned by company.")

        employee = Employee.objects.filter(
            id=data['employee'].id, works_at=data['company'].id)
        if not employee.exists():
            raise serializers.ValidationError(
                "Invalid employee ID or works at another company.")

        return data


class GearLogDetailsSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    device = GearSerializer()
    employee = EmployeeSerializer()
    remaining_days = serializers.SerializerMethodField()

    class Meta:
        model = GearLog
        fields = '__all__'

    def get_remaining_days(self, obj):
        current_date = date.today()
        remaining_days = (obj.checkout_date +
                          timedelta(days=obj.period)) - current_date
        return remaining_days.days if remaining_days.days > 0 else 0
