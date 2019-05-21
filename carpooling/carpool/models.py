import calendar

from django.db import models
from django.core.validators import MinValueValidator

from accounts.models import ProfileUser


# Create your models here.


class Offer(models.Model):
    # get list of day's names from the default python calendar
    REGULARITY = [(str(i), calendar.day_name[i]) for i in range(0,7)]
    TYPE_OF_CONTACT = (
        ('E', 'email'),
        ('PH', 'phone')
    )
    NUMBER_OF_SEATS = [(i, int(i)) for i in range(1, 7)]

    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    # ride_id = 'id - check if you can get it'  # to call it directly in the form, here it'll be automatically created anyways
    driver = models.CharField(max_length=70, blank=False, null=False, default='full_name')
    start_location = models.CharField(max_length=50, default='choose start location')
    destination = models.CharField(max_length=50, default='KBC')
    departure_time = models.TimeField(default='7:00')
    return_time = models.TimeField(default='18:00')
    route = models.TextField(max_length=400, blank=True)
    regularity = models.CharField(max_length=15, choices=REGULARITY, default='__all__')
    type_of_contact = models.CharField(max_length=2, choices=TYPE_OF_CONTACT, default='PH')
    number_of_seats = models.CharField(max_length=1, choices=NUMBER_OF_SEATS, default=1)
    passengers = models.CharField(max_length=70, null=True, default='full_name')
    terms_and_conditions = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"{self.pk} - {self.driver}"


class SeatRequest(models.Model):
    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    passenger = models.CharField(max_length=70, blank=False, null=False, default='full_name')
    ride_id = models.PositiveIntegerField() #check if you can link it to Offer.pk in the form and make it a drop-down menu
    drivers_name = models.CharField(max_length=70, default='full_name', blank=False, null=False) # check if you can make it to auto-populate once a ride_id is selected
    comments = models.TextField(max_length=400, blank=True)
    terms_and_conditions = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"Request from {self.passenger}"


class SeatApprovalRejection(models.Model):
    DECISION = [
        (1, 'Approve'),
        (0, 'Reject')
    ]

    user = models.ForeignKey(SeatRequest, on_delete=models.CASCADE)
    passenger = models.CharField(max_length=70, blank=False, null=False, default='full_name')
    approve_reject = models.CharField(max_length=10, choices=DECISION, default=1)
    comments = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return f"{self.approve_reject.verbose_name}"
