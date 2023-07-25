from django.db import models


# Create your models here.
class TuakaUser(models.Model):
    name = models.CharField(max_length= 100, null=True)
    email = models.CharField(max_length= 100, null=True)
    usercode = models.CharField(max_length= 100, null=True)
    verified = models.BooleanField(default=False, null=True)
    image = models.ImageField(blank=True, null=True, upload_to='profile-uploads/', default='profile.png')
    date_created = models.DateField(auto_now_add= True)

    def __str__(self):
        return f'{self.name} {self.usercode}'