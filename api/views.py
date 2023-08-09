from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response

from . serializers import CompanySerializer, EmployeeSerializer
from . models import Company, Employee


@api_view(['GET'])
def test(request):
    project = {
        'for': 'repliq',
        'aplicant': 'ktm',
        'round': 2,
    }
    return Response(project)


@api_view(['GET', 'POST'])
def company(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


@api_view(['GET', 'PATCH', 'DELETE'])
def company_detail(request, company_id):
    if request.method == 'GET':
        try:
            company = Company.objects.get(id=company_id)
            serializer = CompanySerializer(company, many=False)
            return Response(serializer.data)
        except Company.DoesNotExist:
            return Response({"error": "Company not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':
        data = request.data
        company = Company.objects.get(id=company_id)
        serializer = CompanySerializer(company, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':
        try:
            company = Company.objects.get(id=company_id)
            company.delete()
            return Response({"message": "Company %s deleted!" % company_id}, status=status.HTTP_200_OK)
        except Company.DoesNotExist:
            return Response({"error": "Company not exist!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def employee(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


@api_view(['GET', 'PATCH', 'DELETE'])
def employee_details(request, employee_id):
    if request.method == 'GET':
        try:
            employee = Employee.objects.select_related(
                'works_at').get(id=employee_id)

            serializer = EmployeeSerializer(employee, many=False, context={
                                            'include_works_at': True})

            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':
        data = request.data
        employee = Employee.objects.get(id=employee_id)
        serializer = EmployeeSerializer(employee, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':
        try:
            employee = Employee.objects.get(id=employee_id)
            employee.delete()
            return Response({"message": "Employee %s deleted!" % employee_id}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not exist!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def company_employees(request, company_id):
    employees = Employee.objects.filter(works_at_id=company_id)
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)
