from django.shortcuts import render
from django.http import JsonResponse


def helloworld(request):
    return render(request, 'djanapp/myview.html')


def aj_get_cases(request):
    cases = [
        {
            "case_id": 1,
            "client_data": {
                "first_name": "John",
                "id": 1,
                "last_name": "Testcase",
                "url": "http://localhost:5000/api/v1life-insured/1"
            },
            "client_system_id": None,
            "hq_url": "http://localhost:5000/api/v1/cases/1/hq/"
        },
        {
            "case_id": 2,
            "client_data": {
                "first_name": "Mark",
                "id": 2,
                "last_name": "Smith",
                "url": "http://localhost:5000/api/v1life-insured/2"
            },
            "client_system_id": None,
            "hq_url": "http://localhost:5000/api/v1/cases/2/hq/"
        },
        {
            "case_id": 3,
            "client_data": {
                "first_name": "From",
                "id": 3,
                "last_name": "Server",
                "url": "http://localhost:5000/api/v1life-insured/3"
            },
            "client_system_id": None,
            "hq_url": "http://localhost:5000/api/v1/cases/3/hq/"
        },
    ]
    return JsonResponse(cases, safe=False)
