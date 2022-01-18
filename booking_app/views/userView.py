from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated
#----------------
from booking_app.serializers.userSerializer import UserSerializer
from booking_app.models.userModel import User

class UserCreateView(views.APIView):

    def post(self, request, *args, **kwargs):

        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tokenData = {"dniUser":request.data["dniUser"],"password":request.data["password"]}
        tokenSerializer = TokenObtainPairSerializer(data=tokenData)
        tokenSerializer.is_valid(raise_exception=True)
        return Response(tokenSerializer.validated_data, status=status.HTTP_201_CREATED)

class UserView(views.APIView):

    permission_classes = (IsAuthenticated,)    

    def get(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False) 

        serializer = UserSerializer()
        instance = User(dniUser = valid_data["dni_user"])
        result = serializer.to_representation(instance)

        return Response(result, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        request.data["dniUser"] = valid_data["dni_user"]
        instance = User(dniUser = valid_data["dni_user"])

        serializer = UserSerializer(instance, data=request.data)        
        serializer.is_valid(raise_exception=True)        
        updatedUser = serializer.save()
        result = serializer.to_representation(updatedUser)

        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if valid_data['dni_user'] != kwargs['pk']:
            stringResponse = {'detail':'Unauthorized Request'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        instance = User.objects.get(dniUser= kwargs['pk'])
        instance.delete()

        return Response({"message":"Usuario eliminado correctamente"}, status=status.HTTP_200_OK)