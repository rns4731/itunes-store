from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from store.catalog.models import Album, Artist, Track

class CatalogTests(APITestCase):

    def setUp(self):
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(artist=self.artist, name="Album 1", release_date="2001-09-26", price=12)
        self.track1 = Track.objects.create(album=self.album, title="Track 1", duration=120)
        self.track2 = Track.objects.create(album=self.album, duration=150)
        self.track3 = Track.objects.create(album=self.album, title="Track 3")

    def test_list_artists(self):
        url = reverse("artist-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_create_artist(self):
        url = reverse("artist-list")
        data = {"name": "Test Artist"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Artist.objects.count(), 2)
        self.assertEqual(response.data["name"], "Test Artist")
    
    def test_list_albums_for_artist(self):
        artist = Artist.objects.create(name="Test Artist")
        Album.objects.create(artist=artist, name="Album 1", release_date="2001-09-26", price=12)
        url = reverse("artist-albums", args=[artist.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual("tracks" in response.data[0], False)
    
    def test_list_albums_for_artist_with_tracks(self):
        url = reverse("artist-albums", args=[self.artist.id])
        response = self.client.get(url, {"include_tracklist": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]["tracks"]), 3)
    
    def test_list_albums_for_artist_with_release_date(self):
        url = reverse("artist-albums", args=[self.artist.id])
        response = self.client.get(url, {"release_date": "2001-09-26"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_albums_for_artist_with_price(self):
        url = reverse("artist-albums", args=[self.artist.id])
        response = self.client.get(url, {"price": 12})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_list_albums_for_artist_with_release_date_empty(self):
        url = reverse("artist-albums", args=[self.artist.id])
        response = self.client.get(url, {"release_date": "2001-09-27"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    
    def test_create_album(self):
        artist = Artist.objects.create(name="Test Artist")
        url = reverse("album-list")
        data = {"artist": artist.id, "name": "Album 1", "release_date": "2022-01-01", "price": 12.99}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)
    
    def test_create_album_with_tracks(self):
        artist = Artist.objects.create(name="Test Artist")
        url = reverse("album-list")
        data = {
            "artist": artist.id,
            "name": "Album T",
            "release_date": "2022-01-01",
            "price": 12.99,
            "tracks": [
                {"title": "Track 1", "duration": 120},
                {"title": "Track 2", "duration": 150},
                {"title": "Track 3", "duration": 180}
            ]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Album.objects.count(), 2)
        self.assertEqual(Track.objects.count(), 6)
        album = Album.objects.get(name="Album T")
        self.assertEqual(album.tracks.count(), 3)
