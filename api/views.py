from django.contrib.auth.views import LoginView
from django.shortcuts import render

# Create your views here.
from rest_framework import filters

from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import MovieDetails
from .serializers import MovieDetailsSerializer


class MovieAPI(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MovieDetailsSerializer
    queryset = MovieDetails.objects.all()
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['ratings', 'duration', 'release_data']
    search_fields = ['name', 'description']





