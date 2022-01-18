from datetime import time
from rest_framework import serializers
from booking_app.models.ticketModel import Ticket
from booking_app.models.routeModel import Route
from booking_app.models.userModel import User

class TicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = ['get_ticket', 'dni_User', 'id_trip']

    def create(self, validated_data):
        ticketInstance = Ticket.objects.create(**validated_data)
        return ticketInstance

    def to_representation(self, obj):
        ticket = Ticket.objects.get(id_ticket=obj.id_ticket)
        user = User.objects.get(dniUser=ticket.dni_User)
        route = Route.objects.get(id_trip=ticket.id_trip)
        return {
            "id_ticket": ticket.id_ticket,
            "get": ticket.get_ticket,
            "user": {
                "dniUser": user.dniUser,
                "name": user.name,
                "last": user.last_name,
                "email": user.email,
                'phone': user.phone
            },
            'route': {
                "id_trip": route.id_trip,
                "from": route.t_from,
                "to": route.t_to,
                "date": route.date,
                "duration": route.duration,
                "service": route.service,
                "rate": route.rate,
                "vehicle": route.id_vehicle,
                "company": route.company
            }
        }
    
    def get_element(self, **obj):        
        return Ticket.objects.filter(**obj)

    def delete_element(self, id):
        men = Ticket.objects.get(pk=id)
        men.delete()
        return men

    def company_representation(self, obj):
        ticket = Ticket.objects.get(id_ticket=obj.id_ticket)
        user = User.objects.get(dniUser=ticket.dni_User)
        return {
        "ticket": ticket.id_ticket,
            "get": ticket.get_ticket,
            "user": {
                "dniUser": user.dniUser,
                "name": user.name,
                "last": user.last_name,
                'phone': user.phone
            }
        }