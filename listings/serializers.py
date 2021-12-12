from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from .models import BookingInfo, Listing, Reserved


class BookingInfoSerializer(serializers.ModelSerializer):
    
    listing_type = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    country = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:

        model = BookingInfo
        fields = ["listing_type", "title", "country", "city", "price"]

    def get_listing_type(self, data):
         
        if data.listing:
            return data.listing.listing_type 
        else:
            return data.hotel_room_type.hotel.listing_type

    def get_title(self, data):
        if data.listing:
            return data.listing.title 
        else:
            return data.hotel_room_type.hotel.title

    def get_country(self, data):
        if data.listing:
            return data.listing.country 
        else:
            return data.hotel_room_type.hotel.country

    def get_city(self, data):
        if data.listing:
            return data.listing.city 
        else:
            return data.hotel_room_type.hotel.city