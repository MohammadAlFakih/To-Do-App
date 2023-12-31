from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profiles_pictures')
    def __str__(self):
        return f'{self.user.username} Profile'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        image = Image.open(self.image.path)
        if image.width >300 or image.height >300:
            new_size = (300,300)
            image.thumbnail(new_size)
            image.save(self.image.path)
