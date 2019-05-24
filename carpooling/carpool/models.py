import calendar
import csv

from multiselectfield import MultiSelectField

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import ProfileUser

# from .db_tables import DISTRICTS


# Create your models here.

CSV_PATH = 'carpool/Sofia_districts.csv'  # Csv file path
# flat_list = []

with open(CSV_PATH, newline='') as csvfile:
    rows = csv.reader(csvfile, delimiter=',', quotechar=';')
    districts = list(rows)
    flat_list = [item for sublist in districts[1:] for item in sublist]
    print(flat_list)


class Offer(models.Model):
    DISTRICTS = [(dist, dist) for dist in flat_list]

    # get list of days' names from the default python calendar as tuple
    # REGULARITY = [(str(i), str(calendar.day_name[i])) for i in range(0,7)]
    REGULARITY = (
        ('*', 'All'),
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday')
    )
    TYPE_OF_CONTACT = (
        ('E', 'email'),
        ('PH', 'phone')
    )
    NUMBER_OF_SEATS = [(i, i) for i in range(1, 7)]

    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE, default=1)
    # ride_id = 'id - check if you can get it'  # to call it directly in the form, here it'll be automatically created anyways
    # driver = models.CharField(max_length=70, blank=False, null=False, default='full_name')
    # driver = models.CharField(max_length=70, default=f"{ProfileUser.first_name} {ProfileUser.last_name}")
    start_location = models.CharField(max_length=50, default='choose start location', choices=DISTRICTS)
    destination = models.CharField(max_length=50, default='KBC')
    departure_time = models.TimeField(default='7:00')
    return_time = models.TimeField(default='18:00')
    route = models.TextField(max_length=400, blank=True)
    regularity = MultiSelectField(choices=REGULARITY, default='*')
    type_of_contact = models.CharField(max_length=2, choices=TYPE_OF_CONTACT, default='PH')
    number_of_seats = models.IntegerField(choices=NUMBER_OF_SEATS, default=1)
    car_picture = models.ImageField(upload_to='images/',default='images/default_car.png', null=True, blank=True)
    passengers = models.CharField(max_length=70, null=True, default='full_name')
    terms_and_conditions = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"Offer ID {self.pk} with driver {self.user}"

#
# @receiver(post_save, sender=ProfileUser)
# def create_or_update_offer(sender, instance, created, *args, **kwargs):
#     if not created:
#         return
#     Offer.objects.create(offer=instance)
#
#
# @receiver(post_save, sender=ProfileUser)
# def save_offer(sender, instance, **kwargs):
#     instance.offer.save()
#
#
# post_save.connect(create_or_update_offer, sender=ProfileUser)
#

# https://automotivegroup.co.uk/wp-content/themes/automotive/library/images/z-car-default-ftdimg.jpg

class SeatRequest(models.Model):
    user = models.ForeignKey(ProfileUser, on_delete=models.CASCADE)
    offer = models.ManyToManyField(Offer)
    passenger = models.CharField(max_length=70, blank=False, null=False, default='full_name')
    ride_id = models.ForeignKey(Offer, on_delete=models.CASCADE, related_name='pk')  # check if you can link it to Offer.pk in the form and make it a
    # drop-down menu
    driver = models.CharField(max_length=70, default=f'{user}', blank=False, null=False)  # check if you can make it to auto-populate once a ride_id is selected
    comments = models.TextField(max_length=400, blank=True)
    terms_and_conditions = models.BooleanField(default=False, blank=False)

    def __str__(self):
        return f"Request from {self.passenger}"


class SeatApprovalRejection(models.Model):
    DECISION = [
        ('1', 'Approve'),
        ('0', 'Reject')
    ]

    user = models.ForeignKey(SeatRequest, on_delete=models.CASCADE)
    passenger = models.CharField(max_length=70, blank=False, null=False, default='full_name')
    approve_reject = models.CharField(max_length=10, choices=DECISION, default=1)
    comments = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return f"{self.approve_reject}"
