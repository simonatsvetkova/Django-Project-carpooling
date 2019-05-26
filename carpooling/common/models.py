from django.db import models


# Create your models here.
class FAQ(models.Model):
    question = models.CharField(max_length=255, blank=False, null=False, default='question')
    answer = models.TextField(max_length=1400, blank=False, default='answer')

    def __str__(self):
        return f"{self.id} - {self.question}"
