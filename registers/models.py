from django.db import models

# Create your models here.
from django.contrib.auth.models import User#for profile i need User

from django.dispatch import receiver
from django.db.models.signals import post_save#user object  signal create hunxa




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)#one user have one user nad pw so onetoone field
    fullname = models.CharField(max_length=100,null=True)#null true means use value when needed
    address = models.CharField(max_length=100, null=True)
    contact = models.CharField(max_length=100,null =True)
    email=models.EmailField(max_length=100,null=True)
    
    class Meta:
            verbose_name_plural ='Profile'
        
        
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        
        
    def __str__(self):
        return self.user.username    #i use this function because i dont use null =True in user -everytime i need this
    
    
    @receiver(post_save, sender = User)#post save paxi uend by user
    def update_profile(sender,instance,created,*args,**kwargs):
        if created:
            Profile.objects.create(user=instance)
            instance.profile.save()
            
            
            
            

