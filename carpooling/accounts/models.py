from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class ProfileUser(models.Model):
    # REQUIRED_FIELDS = ('user',)
    # USERNAME_FIELD = 'username'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email = models.EmailField()
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='images/', default='images/default_avatar.jpg', null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

# this saves the user in both groups User (the default Django group) and the ProfileUser group
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, *args, **kwargs):
        if not created:
            return
        ProfileUser.objects.create(user=instance)


    post_save.connect(create_or_update_user_profile, sender=User)
