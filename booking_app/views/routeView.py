from django.conf import settings
from rest_framework import serializers, status, views
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from booking_app.serializers.routeSerializer import RouteSerializer
from booking_app.models.routeModel import Route

class RouteView(views.APIView):

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if int(request.data["id_company"]) != valid_data["dni_user"]:
            stringResponse = {'message':'No está autorizado para agregar una nueva ruta.'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = RouteSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message" : "La ruta fue creada con éxito."}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        serializer = RouteSerializer()
        query = serializer.get_element(id_company=int(valid_data["dni_user"]))

        offer = []
        for r in query:
            offer.append(serializer.to_representation(r))
        
        return Response(offer, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        request.data["id_company"] = valid_data["dni_user"]
        instance = Route(id_trip = request.data["id_trip"])

        serializer = RouteSerializer(instance, data=request.data)        
        serializer.is_valid(raise_exception=True)        
        updatedRoute = serializer.save()
        result = serializer.to_representation(updatedRoute)

        return Response(result, status=status.HTTP_200_OK)
    
    def delete(self, request, *args, **kwargs):
        
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)
        
        data = kwargs['verif'].split('-')
        dniUser = int(data[0])
        idRoute = data[1]

        if dniUser != valid_data["dni_user"]:
            stringResponse = {'message':'No tiene permisos para eliminar esta ruta.'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = RouteSerializer()
        serializer.delete_element(idRoute)
        message = {"message": f"La ruta {idRoute} ha sido eliminada con éxito."}

        return Response(message, status=status.HTTP_200_OK)

class ToUserView(views.APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)  

        routeSerializer = RouteSerializer()
        data = kwargs['query'].split('-')
        t_from = data[0]
        t_to = data[1]
        query_result = routeSerializer.get_element(t_from__icontains=t_from, t_to__icontains=t_to)
        # query_result = routeSerializer.get_element(t_from__icontains=request.data["t_from"], t_to__icontains=request.data["t_to"])
        if query_result.count() == 0:
                stringResponse = {'message':'La busqueda no coincide con alguna ruta.'}
                return Response(stringResponse, status=status.HTTP_404_NOT_FOUND)

        routes = []
        for r in query_result:
            routes.append(routeSerializer.to_representation(r))
        
        return Response(routes, status=status.HTTP_200_OK)