from django.contrib import admin
from .models.userModel import User
from .models.ticketModel import Ticket
from .models.routeModel import Route

# Register your models here.
admin.site.register(User)
admin.site.register(Ticket)
admin.site.register(Route)