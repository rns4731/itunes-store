from rest_framework import serializers

from store.catalog.models import Album, Artist, Track


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Album
        fields = ['id', 'artist', 'name', 'release_date', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.context.get('include_tracklist', False):
            self.fields['tracks'] = TrackSerializer(many=True, read_only=True)


class AlbumCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ['artist', 'name', 'release_date', 'price']


class TrackCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['title', 'duration']
