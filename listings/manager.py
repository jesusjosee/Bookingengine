from django.db import models

class ListingManager(models.Manager):
    
    def get_price(self, max_price):

        queryset = self.filter(booking_info__price__lte = max_price)
        return queryset