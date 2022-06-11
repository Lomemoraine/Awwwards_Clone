from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    bio = models.CharField(default="Welcome", max_length = 40)
    picture = CloudinaryField('images', default='https://res.cloudinary.com/dcfb3gqzg/image/upload/v1654542339/bclz5p1q2ch81qz9ukpz.jpg')
    
    def __str__(self):
        return f'{self.user.username} Profile'
