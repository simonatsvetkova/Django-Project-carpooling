from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class ProfileUser(models.Model):
    # REQUIRED_FIELDS = ('user',)
    # USERNAME_FIELD = 'username'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    # username = User.username
    # profile_picture = models.URLField(default='https://upload.wikimedia.org/wikipedia/common/7/72/Default-welcomer.png')
    profile_picture = models.ImageField(upload_to='images/', default='https://upload.wikimedia.org/wikipedia/common/7/72/Default-welcomer.png')

    def __str__(self):
        return f"{self.user}"

# this saves the user in both groups User (the default Django group) and the ProfileUser group
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, *args, **kwargs):
    if not created:
        return
    ProfileUser.objects.create(user=instance)


post_save.connect(create_or_update_user_profile, sender=User)
