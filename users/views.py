import secrets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from idance.utils import CustomModelViewSet
from .models import CustomUser
from post_office import mail
from django.conf import settings

from .serializers.user import UserCreateSerializer, UserSerializer, UserRetrieveSerializer, UserResetPasswordSerializer
from rest_framework import permissions, status


# Create your views here.
@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        identifier = request.data.get('identifier')
        is_phone_number = False

        try:
            user = CustomUser.objects.get(phone_number=identifier)
            is_phone_number = True
        except CustomUser.DoesNotExist:
            try:
                user = CustomUser.objects.get(email=identifier)
            except CustomUser.DoesNotExist:
                user = None

        if user:
            new_password = secrets.token_urlsafe(8)
            user.set_unusable_password()
            user.set_password(new_password)
            user.save()
            if is_phone_number:
                return Response({'message': 'Password reset successfully', 'is_phone_number': True},
                                status=status.HTTP_200_OK)
            else:
                subject = 'Сброс пароля'
                message = f'Ваш новый пароль: {new_password}'
                html_message = f'Ваш новый пароль: {new_password}'

                mail.send(
                    email,
                    settings.DEFAULT_FROM_EMAIL,
                    subject=subject,
                    message=message,
                    html_message=html_message,
                    priority='now'
                )
                return Response({'message': 'Password reset successfully', 'is_phone_number': False},
                                status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User with such email or phone number not found'},
                            status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def register(request):
    serializer = UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'user': serializer.data, 'message': 'User registered successfully'},
                        status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(CustomModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    serializer_list = {
        'retrieve': UserRetrieveSerializer,
        'create': UserCreateSerializer,
        'reset-password': UserResetPasswordSerializer,
    }
    permission_classes = [permissions.IsAuthenticated]
