from django.urls import path,include

from rest_framework.routers import DefaultRouter
from myapp import views

router = DefaultRouter()

router.register("zone", views.ZoneApi, basename="zone")
router.register("state", views.StateApi, basename="state")
router.register("district", views.DistrictApi, basename="Distrcit")

urlpatterns = [
    path("login/",views.login.as_view()),
    path('home/',views.home.as_view())
] + router.urls