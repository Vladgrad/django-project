from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Coworking, Desk, Booking
from .serializers import (
    RegisterSerializer, CoworkingSerializer, 
    DeskSerializer, BookingSerializer
)
from api.permissions import IsAdminOrReadOnly, IsOwnerOrAdmin


class RegisterApiView(APIView):
       
       permission_classes = [permissions.AllowAny]
       
       def post(self, request):
              serializer = RegisterSerializer(data=request.data)
              if serializer.is_valid():
                     user = serializer.save()
                     return Response({
                            'message': 'Пользоваткль зарегестрирован',
                            'data': {'id': user.id, 'email': user.email}
                     }, status=status.HTTP_201_CREATED)
              return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
       
class LoginApiView(APIView):
       permission_classes = [permissions.AllowAny]
       
       def post(self, request):
              email = request.data.get('email')
              password = request.data.get('password')
              user = authenticate(username=email, password=password)
              
              if user:
                     refresh = RefreshToken.for_user(user)
                     return Response({
                            'message': 'Успешно авторизовались',
                            'data': {'token': str(refresh.access_token)}
                     })
              return Response({'message': 'Неверные учетные данные'}, status=401)
       
       
       
class CoworkingApiView(viewsets.ModelViewSet):
       queryset = Coworking.objects.all()
       serializer_class = CoworkingSerializer
       permission_classes = [IsAdminOrReadOnly]
       
       
class DeskApiView(viewsets.ModelViewSet):
       queryset = Desk.objects.all()
       serializer_class = DeskSerializer
       permission_classes = [IsAdminOrReadOnly]
       
       
class BookingApiView(viewsets.ModelViewSet):
       serializer_class = BookingSerializer
       permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
       
       
       def get_queryset(self):
              if self.requets.user.is_staff:
                     return Booking.objects.all()
              return Booking.objects.filter(client=self.request.user)
       
       
       def perform_create(self, serializer):
              serializer.save(client=self.request.user)
              
              
       def create(self, request, *args, **kwargs):
              try:
                     return super().create(request, *args, **kwargs)
              except Exception as e:
                     if 'Заблокировано' in str(e):
                            return Response({
                                   'message': 'Слот уже занят',
                                   'errors': [{'field': 'desk', 'code': 'slot_conflict', 'detail': str(e)}]
                            }, status=status.HTTP_409_CONFLICT)
                     raise e
              
       @action(detail=True, methods=['post'])
       def cansel(self, request, pk=None):
              booking = self.get_object()
              if booking.status == 'cancelled':
                     return Response({'message': 'Бронь уже отменена'}, status=409)
              booking.status = 'cancelled'
              booking.save()
              return Response({'booking_id': booking.booking_id, 'status': 'cancelled'})
                     