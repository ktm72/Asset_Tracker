from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, F
from django.utils.dateparse import parse_date
from datetime import date, timedelta

from . serializers import CompanySerializer, EmployeeCreateSerializer, EmployeeSerializer, GearSerializer, GearCreateSerializer, GearLogSerializer, GearLogCreateSerializer
from . models import Company, Employee, Gear, GearLog


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
        total = companies.count()

        serializer = CompanySerializer(companies, many=True)
        return Response({"total_results": total, "results": serializer.data})

    elif request.method == 'POST':
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def company_details(request, company_id):
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
        total = employees.count()

        serializer = EmployeeSerializer(employees, many=True)
        return Response({"total_results": total, "results": serializer.data})

    elif request.method == 'POST':
        serializer = EmployeeCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def employee_details(request, employee_id):
    if request.method == 'GET':
        try:
            employee = Employee.objects.select_related(
                'works_at').get(id=employee_id)
            serializer = EmployeeSerializer(employee, many=False, context={
                                            'include_company_details': True})

            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':
        data = request.data
        employee = Employee.objects.get(id=employee_id)
        serializer = EmployeeCreateSerializer(
            employee, data=data, partial=True)

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

    status_param = request.query_params.get('status', '').lower()

    if status_param == 'true':
        query = Q(works_at_id=company_id) & Q(status=True)
        employees = Employee.objects.filter(query)

    elif status_param == 'false':
        query = Q(works_at_id=company_id) & Q(status=False)
        employees = Employee.objects.filter(query)

    else:
        employees = Employee.objects.filter(works_at_id=company_id)

    total = employees.count()
    serializer = EmployeeSerializer(employees, many=True)

    return Response({"total_results": total, "results": serializer.data})


@api_view(['GET', 'POST'])
def gear(request):
    if request.method == 'GET':

        gear = Gear.objects.all()
        total = gear.count()

        serializer = GearSerializer(gear, many=True)
        return Response({"total_results": total, "results": serializer.data})

    elif request.method == 'POST':
        serializer = GearCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def gear_details(request, gear_id):
    if request.method == 'GET':
        try:
            gear = Gear.objects.select_related('owner').get(id=gear_id)
            serializer = GearSerializer(gear, many=False, context={
                'include_owner_details': True})
            return Response(serializer.data)
        except Gear.DoesNotExist:
            return Response({"error": "Gear not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':
        data = request.data
        gear = Gear.objects.get(id=gear_id)
        serializer = GearSerializer(gear, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':
        try:
            gear = Gear.objects.get(id=gear_id)
            gear.delete()
            return Response({"message": "Gear %s deleted!" % gear_id}, status=status.HTTP_200_OK)
        except Gear.DoesNotExist:
            return Response({"error": "Gear not exist!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def company_gears(request, company_id):
    gears = Gear.objects.filter(owner_id=company_id)
    total = gears.count()

    serializer = GearSerializer(gears, many=True)
    return Response({"total_results": total, "results": serializer.data})


@api_view(['GET', 'POST'])
def gear_log(request):
    if request.method == 'GET':

        returned = request.query_params.get('returned', '')
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get(
            'end_date', date.today().isoformat())

        filters = Q()
        if returned:
            filters &= Q(returned=returned.lower() == 'true')

        if start_date_str and end_date_str:
            start_date = parse_date(start_date_str)
            end_date = parse_date(end_date_str)
            filters &= Q(returned_date__range=[start_date, end_date])

        log = GearLog.objects.all().filter(filters)
        total = log.count()

        serializer = GearLogSerializer(log, many=True)
        return Response({"total_results": total, "results": serializer.data})

    if request.method == 'POST':
        serializer = GearLogCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
def gear_log_details(request, log_id):
    if request.method == 'GET':
        try:
            log = GearLog.objects.get(id=log_id)
            serializer = GearLogSerializer(log, many=False, context={
                                           'include_details': True})
            return Response(serializer.data)
        except GearLog.DoesNotExist:
            return Response({"error": "GearLog not found"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':
        data = request.data
        log = GearLog.objects.get(id=log_id)
        serializer = GearLogCreateSerializer(log, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'DELETE':
        try:
            log = GearLog.objects.get(id=log_id, returned=True)
            log.delete()
            return Response({"message": "GearLog %s deleted!" % log_id}, status=status.HTTP_200_OK)
        except GearLog.DoesNotExist:
            return Response({"error": "Log deleted or not returned!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def company_logs(request, company_id):

    returned = request.query_params.get('returned', '')
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get(
        'end_date', date.today().isoformat())

    filters = Q(company_id=company_id)
    if returned:
        filters &= Q(returned=returned.lower() == 'true')

    if start_date_str and end_date_str:
        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)
        filters &= Q(returned_date__range=[start_date, end_date])

    logs = GearLog.objects.filter(filters)
    total = logs.count()

    serializer = GearLogSerializer(logs, many=True)
    return Response({"total_results": total, "results": serializer.data})


@api_view(['GET'])
def employee_logs(request, employee_id):
    returned = request.query_params.get('returned', '')
    filters = Q(employee_id=employee_id)
    if returned:
        filters &= Q(returned=returned.lower() == 'true')
    logs = GearLog.objects.filter(filters)
    total = logs.count()

    serializer = GearLogSerializer(logs, many=True)
    return Response({"total_results": total, "results": serializer.data})
