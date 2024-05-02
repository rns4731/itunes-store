# iTunes Store API

This is an API for creating an iTunes like store using Django and Django rest framework.

## Setup


This project uses python3, make sure you have python3 installed in your OS: https://www.python.org/downloads/.


Set up the project using a python virtual environment:

```
python3 -m venv /path/to/new/virtual/environment
source <venv>/bin/activate
which python3
 /path/to/new/virtual/environment/bin/python
```

## Requirements

Requirements are listed in `requirements.txt`. Install the requirements from the root folder:

```
pip install requirements.txt
```

## Start server

Once requirements have been installed, start the Django server:

```
python manage.py runserver
```


Now you should be able to access the following endpoints available for testing.

GET http://127.0.0.1:8000/api/artists/ - get a list of artists

GET http://127.0.0.1:8000/api/artists/:artistid/albums - get a list of albums for the artist

GET http://127.0.0.1:8000/api/artists/:artistid/albums?include_tracklist=true - get a list of albums for the artist with tracks

GET http://127.0.0.1:8000/api/artists/:artistid/albums?release_date=:string - get a list of albums for the artist filtered by release date

GET http://127.0.0.1:8000/api/artists/:artistid/albums?price=:number - get a list of albums for the artist filtered by price

POST http://127.0.0.1:8000/api/artists/ - create an artist
```
{
    "name": "Spinning disc",
}
```


POST http://127.0.0.1:8000/api/albums/ - create an album with the following json payload, ensure the artist has already been created.
```
{
    "artist": 3,
    "name": "Album1",
    "release_date": "2012-01-01",
    "price": 34,
    "tracks": [
        {
            "duration": 123,
            "title": "t1"
        }
    ]
}

```


## Testing

Test the server by running the following command from the root folder.

```
python manage.py test
```
