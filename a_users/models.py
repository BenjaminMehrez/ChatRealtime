from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from environ import Env
env = Env()
Env.read_env()

ENVIRONMENT = env('ENVIRONMENT', default='production')
if ENVIRONMENT == 'production':
    from cloudinary.models import CloudinaryField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    if ENVIRONMENT == 'production':
        image = CloudinaryField(null=True, blank=True)
    else:
        image = models.ImageField(upload_to='avatars/', null=True, blank=True) # blank signify that can is empty, null can save something empty
    displayname = models.CharField(max_length=20, null=True, blank=True)
    info = models.TextField(null=True, blank=True)
    
    
    def __str__(self):
        return str(self.user)
    
    
    @property
    def name(self):
        if self.displayname:
            return self.displayname
        return self.user.username
    
    
    @property
    def avatar(self):
        if self.image:
            return self.image.url
        return f'{settings.STATIC_URL}images/avatar_default.svg'