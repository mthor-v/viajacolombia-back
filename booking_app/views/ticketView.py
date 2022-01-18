from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework.permissions import IsAuthenticated

from booking_app.serializers.ticketSerializer import TicketSerializer
from booking_app.serializers.routeSerializer import RouteSerializer
from booking_app.models.ticketModel import Ticket

class TicketView(views.APIView):

    permissions_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        if int(request.data["dni_User"]) != valid_data["dni_user"]:
            stringResponse = {'message':'No está autorizado para reservar el tiquete'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TicketSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message':'Reserva creada correctamente'}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        serializer = TicketSerializer()
        query = serializer.get_element(get_ticket=kwargs['verif'], dni_User=valid_data["dni_user"])

        tickets = []
        for t in query:
            tickets.append(serializer.to_representation(t))
        
        return Response(tickets, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        print(request.data["dni_User"],valid_data["dni_user"])

        if int(request.data["dni_User"]) != int(valid_data["dni_user"]):
            stringResponse = {'message':'No está autorizado para modificar la reserva.'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        instance = Ticket(id_ticket= request.data["id_ticket"])

        serializer = TicketSerializer(instance, data=request.data)     
        serializer.is_valid(raise_exception=True)        
        serializer.save()

        stringResponse = {'message':'Tiquete actualizado con éxito.'}

        return Response(stringResponse, status=status.HTTP_200_OK)
    
    
    def delete(self, request, *args, **kwargs):
        
        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)

        data = kwargs['verif'].split('-')
        dniUser = int(data[0])
        idTicket = data[1]

        if dniUser != valid_data["dni_user"]:
            stringResponse = {'message':'No está autorizado para eliminar la reserva.'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TicketSerializer()
        serializer.delete_element(idTicket)
        stringResponse  = {"message": f"El ticket {idTicket} ha sido eliminado con éxito."}

        return Response(stringResponse, status=status.HTTP_200_OK)

class ToCompanyView(views.APIView):

    permissions_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):

        token = request.META.get('HTTP_AUTHORIZATION')[7:]
        tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
        valid_data = tokenBackend.decode(token,verify=False)  

        routeSerializer = RouteSerializer()
        query_result = routeSerializer.get_element(id_company=valid_data["dni_user"], id_trip=kwargs["idTrip"])

        if query_result.count() == 0:
            stringResponse = {'detail':'No está autorizado para ver la información de la ruta'}
            return Response(stringResponse, status=status.HTTP_401_UNAUTHORIZED)

        serializer = TicketSerializer()
        query = serializer.get_element(id_trip=kwargs["idTrip"])

        tickets = []
        for t in query:
            tickets.append(serializer.company_representation(t))
        
        return Response(tickets, status=status.HTTP_200_OK)