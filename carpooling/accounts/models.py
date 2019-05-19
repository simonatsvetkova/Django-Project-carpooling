from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ProfileUser(models.Model):
    # REQUIRED_FIELDS = ('user',)
    # USERNAME_FIELD = 'username'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # username = User.username
    # profile_picture = models.URLField(default='https://upload.wikimedia.org/wikipedia/common/7/72/Default-welcomer.png')
    profile_picture = models.ImageField(upload_to='images/', default='https://upload.wikimedia.org/wikipedia/common/7/72/Default-welcomer.png')

    def __str__(self):
        return f"{self.user}"
