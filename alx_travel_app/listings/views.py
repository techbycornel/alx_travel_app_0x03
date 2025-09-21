from django.http import JsonResponse

def listing_list(request):
    data = [
        {"id": 1, "title": "Beach Resort", "price": 200},
        {"id": 2, "title": "Mountain Cabin", "price": 150},
    ]
    return JsonResponse(data, safe=False)
