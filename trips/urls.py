from django.urls import path
from . import views

app_name = "trips"

urlpatterns = [
    
    path("", views.trip_home, name="trip_home"),

    path("home/", views.trip_redirect, name="trip_redirect"),
    
    path(
    "<int:trip_id>/",
    views.trip_detail,
    name="trip_detail",
    ),

    path(
    "class-method-demo/",
    views.TripMethodView.as_view(),
    name="class_method_demo",
    ),

    path(
    "search/",
    views.trip_search,
    name="trip_search",
    ),

    path(
    "create-demo/",
    views.trip_create_demo,
    name="trip_create_demo",
    ),
   


]