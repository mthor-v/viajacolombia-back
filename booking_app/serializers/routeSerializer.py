from rest_framework import serializers
from booking_app.models.routeModel import Route

class RouteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Route
        fields = ['id_trip', 't_from', 't_to', 'date', 'duration', 'service', 'rate', 'id_vehicle', 'company','id_company']

    def create(self, validated_data):
        routeInstance = Route.objects.create(**validated_data)
        return routeInstance

    def to_representation(self, obj):
        route = Route.objects.get(id_trip=obj.id_trip)
        return {
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
    
    def get_element(self, **obj):        
        return Route.objects.filter(**obj)

    def delete_element(self, id):
        men = Route.objects.get(pk=id)
        men.delete()
        return men