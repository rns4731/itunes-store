from datetime import datetime
from rest_framework import viewsets
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from store.catalog.models import Artist, Album, Track
from store.catalog.serializers import AlbumCreateSerializer, AlbumSerializer, ArtistSerializer
import logging

logger = logging.getLogger(__name__)


class AristViewSet(CreateModelMixin, ListModelMixin, viewsets.GenericViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Creating a new Artist")
        return super().create(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        logger.info("Listing all Artists")
        return super().list(request, *args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def albums(self, request, pk=None):
        artist = self.get_object()
        self.queryset = self.queryset.filter(id=artist.id)
        include_tracklist = request.query_params.get('include_tracklist', False)
        if include_tracklist:
            include_tracklist = include_tracklist.lower() == 'true'
        release_date = request.query_params.get('release_date', None)
        if release_date:
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
            self.queryset = self.queryset.filter(albums__release_date=release_date)
        price = request.query_params.get('price', None)
        if price:
            self.queryset = self.queryset.filter(albums__price=price)

        logger.info("Listing all Albums for Artist %s", artist.name)
        albums = Album.objects.filter(artist=self.queryset.first())
        if include_tracklist:
            albums = albums.prefetch_related('tracks')
            serializer = AlbumSerializer(albums, many=True, context={'include_tracklist': True})
        else:
            serializer = AlbumSerializer(albums, many=True)

        return Response(serializer.data)


class AlbumViewSet(CreateModelMixin,viewsets.GenericViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def create(self, request, *args, **kwargs):
        logger.info("Creating a new Album")
        request_data = request.data.copy()
        tracks = request_data.pop('tracks', [])
        serializer = AlbumCreateSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        album = serializer.save()
        
        for track in tracks:
            track['album_id'] = album.id
            Track.objects.create(**track)

        return Response(AlbumSerializer(album, context={'include_tracklist': True}).data, status=201)

        
