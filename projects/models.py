from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    bio = models.CharField(default="Welcome", max_length = 40)
    picture = CloudinaryField('images', default='http://res.cloudinary.com/dim8pysls/image/upload/v1639001486/x3mgnqmbi73lten4ewzv.png')
    
    def __str__(self):
        return f'{self.user.username} Profile'
