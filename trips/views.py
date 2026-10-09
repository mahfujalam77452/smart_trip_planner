from django.shortcuts import render
<<<<<<< HEAD
import json
=======
from django.http import JsonResponse
from django.shortcuts import redirect

>>>>>>> 726ca96 (refactor: add trip URL namespace and redirect)
# Create your views here.
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

def trip_home(request):
    return JsonResponse({
        "message": "Welcome to Smart Trip Planner",
        "status": "success",
    })


def trip_redirect(request):
    return redirect("trips:trip_home")

def trip_detail(request, trip_id):
    return JsonResponse({
        "message": "Trip details",
        "trip_id": trip_id,
    })
@method_decorator(csrf_exempt, name="dispatch")
class TripMethodView(View):

    def get(self, request):
        return JsonResponse({
            "message": "Fetching trips",
        })

    def post(self, request):
        return JsonResponse({
            "message": "Creating a trip",
        }, status=201)


def trip_search(request):
    destination = request.GET.get("destination", "")
    max_budget = request.GET.get("max_budget")

    return JsonResponse({
        "destination": destination,
        "max_budget": max_budget,
    })




def trip_create_demo(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    destination = data.get("destination")
    budget = data.get("budget")

    if not destination or budget is None:
        return JsonResponse(
            {"error": "destination and budget are required"},
            status=400,
        )

    return JsonResponse(
        {
            "message": "Input received successfully",
            "destination": destination,
            "budget": budget,
        },
        status=201,
    )

<<<<<<< HEAD

@csrf_exempt
def trip_create_demo(request):

    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    destination = data.get("destination")
    budget = data.get("budget")

    if not destination or budget is None:
        return JsonResponse(
            {"error": "destination and budget are required"},
            status=400,
        )

    return JsonResponse(
        {
            "message": "Input received successfully",
            "destination": destination,
            "budget": budget,
        },
        status=201,
    )


=======
def trip_redirect(request):
    return redirect("trips:trip_home")
>>>>>>> 726ca96 (refactor: add trip URL namespace and redirect)
