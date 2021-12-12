from django.shortcuts import render


from rest_framework.generics import  ListAPIView

from .models import BookingInfo, Listing, Reserved


from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

from listings.serializers import BookingInfoSerializer

class RoomsAvailableView(APIView):
    
    def get(self, request):

        # Get the date range and max_price
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        max_price = request.query_params.get('max_price')

        # Filter rooms below max_price and sort by lower to higher price
        rooms_below_max_price = BookingInfo.objects.filter(price__lte=max_price).order_by('price')

        # Filter Reserved rooms
        reserved_rooms = Reserved.objects.filter(
            Q(check_in__lte=check_in, check_out__gte=check_in) | 
            Q(check_in__lte=check_out, check_out__gte=check_out) | 
            Q(check_in__gte=check_in, check_out__lte=check_out)).values_list('booking_info_id', flat=True)

        # Exclude reserved rooms from rooms left below max_price
        available_rooms = rooms_below_max_price.exclude(id__in=reserved_rooms)

        if not available_rooms:
            return Response({"msg": "No rooms available!"}, status=status.HTTP_200_OK)

        # List unreserved rooms
        available_rooms_listing = BookingInfoSerializer(available_rooms, many=True).data
        
        return Response({"items": available_rooms_listing}, status=status.HTTP_200_OK)