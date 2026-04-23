from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
       RegisterApiView, LoginApiView, CoworkingApiView, DeskApiView, BookingApiView
)

router = DefaultRouter()
router.register(r'coworkings', CoworkingApiView, basename='coworking')
router.register(r'desks', DeskApiView, basename='desk')
router.register(r'bookings', BookingApiView, basename='booking')

urlpatterns = [
    path('auth/register/', RegisterApiView.as_view(), name='register'),
    path('auth/login/', LoginApiView.as_view(), name='login'),
    
    path('api/', include(router.urls))

]