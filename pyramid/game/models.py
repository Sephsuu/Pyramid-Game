from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Students(models.Model):
    stud_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)

class Vote(models.Model):
    voter = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='voter')
    recipient = models.ForeignKey(Students, on_delete=models.CASCADE, related_name='recipient')
    vote_count = models.IntegerField(default=0)

    class Meta:
        unique_together = ('voter', 'recipient')
