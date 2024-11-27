from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


UserModel = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "phone_number"

    def validate(self, attrs):
        phone_number = attrs.get(self.username_field)
        password = attrs.get("password")

        if not phone_number or not password:
            raise serializers.ValidationError("Both phone_number and password are required.")

        try:
            user = UserModel.objects.get(phone_number=phone_number)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("User with this phone number does not exist.")

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")

        data = super().validate({
            "phone_number": phone_number, 
            "password": password,
        })

        return data

class CustomRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    email = serializers.EmailField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = UserModel
        fields = ('phone_number', 'email', 'password1', 'password2')

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if UserModel.objects.filter(phone_number=data['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "Phone number is already in use."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password1')
        user = UserModel.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class CustomLoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = authenticate(phone_number=phone_number, password=password)

        if not user:
            raise serializers.ValidationError('Invalid phone number or password')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')
        
        attrs['user'] = user
        return attrs

