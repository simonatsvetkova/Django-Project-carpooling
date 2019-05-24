from django.contrib import admin

from .models import Offer, SeatRequest, SeatApprovalRejection

# Register your models here.
admin.site.register(Offer)
admin.site.register(SeatRequest)
admin.site.register(SeatApprovalRejection)