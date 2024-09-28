from django.db import models
from django.contrib.auth.models import User
import shortuuid
import os
from PIL import Image
import cloudinary.uploader

from environ import Env
env = Env()
Env.read_env()
ENVIRONMENT = env('ENVIRONMENT', default='production')
if ENVIRONMENT == 'production':
    from cloudinary.models import CloudinaryField

# Create your models here.

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    groupchat_name = models.CharField(max_length=128, null=True, blank=True)
    admin = models.ForeignKey(User, related_name='groupchats', blank=True, null=True, on_delete=models.SET_NULL)
    users_online = models.ManyToManyField(User, related_name='online_in_groups', blank=True)
    members = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    is_private = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.group_name)
    
    
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    if ENVIRONMENT == 'production':
        file = CloudinaryField(null=True, blank=True)
    else:
        file = models.FileField(upload_to='files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    

    @property
    def filename(self):
        if self.file:
            try:
                # En producción o desarrollo, obtenemos la URL del archivo en lugar del 'name'
                return self.file.url
            except Exception as e:
                print(f"Error obteniendo la URL del archivo: {str(e)}")
                return None
        else:
            print("No se proporcionó ningún archivo.")
            return None
    
    class Meta:
        ordering = ['-created']
        
    @property    
    def is_image(self):
        if self.file:
            # Para Cloudinary, verificamos la extensión desde la URL en lugar de intentar abrir el archivo
            file_extension = os.path.splitext(self.file.url)[1].lower()
            return file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return False