from django.http import JsonResponse

def index(request):
    return JsonResponse({"message": "Welcome to ALX Travel App Listings API"})
