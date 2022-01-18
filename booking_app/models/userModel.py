from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):

    def create_user(self, dniUser, password=None):
        if not dniUser:
            raise ValueError('Users must have an dniUser')
        user = self.model(dniUser=dniUser) #model se hereda de BaseUserManager
        user.set_password(password)
        user.save(using=self._db) # ORM inserta usuario en base de datos
        return user
            
    def create_superuser(self, dniUser, password):

        user = self.create_user(
            dniUser=dniUser,
            password=password,
        ) # rehuso el primer metodo
        user.is_admin = True # Le ofrezco privilegios de admin
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):

    dniUser = models.BigIntegerField('dniUser', null=False, primary_key=True)
    password = models.CharField('Password', max_length = 256, null=False)
    name = models.CharField('Name', max_length = 40, null=False)
    last_name = models.CharField('Name', max_length = 40, blank= True)
    email = models.EmailField('Email', max_length = 100, unique=True, null=False)
    phone = models.BigIntegerField('Phone', blank=True, null=False)
    role = models.CharField('Role', max_length=8, default="Usuario")
    # se sobreescribe la función para encriptar la contraseña en la bd
    def save(self, **kwargs): # ** -> recibe un diccionario
        if not self.password:
            raise ValueError('Users must have an password')
        some_salt = 'mMUj0DrIK6vgtdIYepkIxN' # Valor secreto para cifrado
        self.password = make_password(self.password, some_salt) # Cifra la contraseña ingresada
        super().save(**kwargs)
        
    objects = UserManager()
    USERNAME_FIELD = 'dniUser'