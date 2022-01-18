from django.db import models

class Route(models.Model):
    SERV_TYPES = (
        ('Basic','Basic'),
        ('Premium','Premium'),
        ('Elite','Elite'),
    )
    id_trip = models.CharField('idTrip', max_length=20 ,unique=True, null=False, primary_key=True)
    t_from = models.CharField('From', max_length=30, null=False)
    t_to = models.CharField('To', max_length=30, null=False)
    date = models.CharField('Date', max_length=18, null=False) 
    duration = models.CharField('Duration', max_length=6, default= "00:00")
    service = models.CharField('Service', max_length=8, choices=SERV_TYPES, default= "Basic")
    rate = models.IntegerField('Rate', null=False)
    id_vehicle = models.CharField('idCar', max_length=10, null=True)
    company = models.CharField('Company', max_length=40, null= False)
    id_company = models.BigIntegerField('idCompany', null=False, default=1)
