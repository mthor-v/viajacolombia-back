from django.db import models

class Ticket(models.Model):
    id_ticket = models.AutoField('idTicket', primary_key=True)
    get_ticket = models.BooleanField('Get', default=False)
    dni_User = models.IntegerField('User', null= False)
    id_trip = models.CharField('idTrip', max_length=20 , null=False)