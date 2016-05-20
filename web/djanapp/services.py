import requests


def get_cases():
    url = 'http://jsonplaceholder.typicode.com/posts/1'
    r = requests.get(url)

    # Mock Data:
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
    return cases
