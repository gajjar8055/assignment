from rest_framework import serializers

from api.models import MovieDetails


class MovieDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = MovieDetails
