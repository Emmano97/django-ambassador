from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from common.authentication import JWTAuthentication
from common.serializers import UserSerializer
from core.models import User


class RegisterAPIView(APIView):

    def post(self, request):
        data = request.data

        if data['password'] != data['password_confirm']:
            raise exceptions.APIException("Password do not match!")

        data['is_ambassador'] = 'api/ambassador' in request.path

        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("Incorrect  password")

        scope = 'ambassador' if 'api/ambassador' in request.path else 'admin'
        
        token = JWTAuthentication.generate_jwt(user.id, scope)

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            'message': 'logged on!'
        }

        return response


class UserAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = UserSerializer(user).data
        if 'api/ambassador' in request.path:
            data['revenue'] = user.revenue

        return Response(data)


class LogoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = Response()

        response.delete_cookie(key="jwt")

        request.user = None

        response.data = {
            'message': "logged out!"
        }
        return response


class ProfileInfoAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk=None):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class ProfilePasswordAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request,  pk=None):
        user = request.user
        data = request.data

        if data["password"] != data["password_confirm"]:
            raise exceptions.APIException("Password do not match!")

        user.set_password(data['password'])

        user.save()

        return Response(UserSerializer(user).data)
