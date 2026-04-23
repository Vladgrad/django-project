from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from .models import Coworking, Desk, Booking

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class CoworkingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coworking
        fields = ['id', 'title', 'city', 'address']

class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ['desk_id', 'coworking', 'name', 'capacity', 'is_active', 'created_at']
        read_only_fields = ['desk_id', 'created_at']

class BookingSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = ['booking_id', 'desk', 'client', 'date', 'slot', 'status', 'created_at']
        read_only_fields = ['booking_id', 'status', 'created_at']

    def validate(self, data):

        exists = Booking.objects.filter(
            desk=data['desk'],
            date=data['date'],
            slot=data['slot'],
            status='active'
        ).exists()

        if exists:
            raise serializers.ValidationError("На это время место уже забронировано")
        
        return data
