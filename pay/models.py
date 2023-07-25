from django.db import models

# Create your models here.
class MemberBusiness(models.Model):
    client_id = models.CharField(null=True, max_length=100)
    client_name = models.CharField(null=True, max_length=100)
    member_id = models.CharField(null=True, max_length=100)
    member_name = models.CharField(max_length= 100, null=True)
    usercode = models.CharField(max_length= 100, null=True)
    date_created = models.DateTimeField(auto_now_add= True)


    def __str__(self):
        return f'{self.member_name} - {self.client_name}'

