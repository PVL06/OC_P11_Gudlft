import pytest

from server import create_app
from utilities import Clubs, Competitions


@pytest.fixture
def clubs():
    clubs = Clubs()
    clubs.clubs = [
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "20"
        }
    ]
    return clubs


@pytest.fixture
def competitions():
    competitions = Competitions()
    competitions.competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
    return competitions


@pytest.fixture
def client(clubs, competitions):
    app = create_app(clubs, competitions)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestIntegrationServer:

    def test_login_with_valid_email(self, client, clubs, competitions):
        credential = {
            'email': clubs.clubs[0]['email']
        }

        res = client.post('/showSummary', data=credential)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find(f"<h2>Welcome, { clubs.clubs[0]['email'] } </h2>") != -1
        assert data.find(f"{ competitions.competitions[0]['name'] }<br />") != -1

    def test_login_with_invalid_email(self, client):
        credential = {
            'email': 'bad@email.com'
        }

        res = client.post('/showSummary', data=credential)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<li>Email not found</li>') != -1
        assert data.find('<title>GUDLFT Registration</title>') != -1

    def test_book_reservation_with_valid_club_and_competition(self, client, clubs, competitions):
        competition = competitions.competitions[0]['name']
        club = clubs.clubs[0]['name']
        res = client.get(f'/book/{competition}/{club}')
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find(f'<title>Booking for {competition} || GUDLFT</title>') != -1

    def test_book_reservation_with_invalid_club_or_competition(self, client):
        res = client.get('/book/invalid_competition/invalid_club')
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<li>Something went wrong-please try again</li>') != -1
        assert data.find('<title>Summary | GUDLFT Registration</title>') != -1

    def test_purchase_place_with_invalid_club_and_competition(self, client, clubs, competitions):
        post_data = {
            'club': 'invalid_club',
            'competition': 'invalid_competition',
            'places': '10'
        }

        res = client.post('/purchasePlaces', data=post_data, follow_redirects=True)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('GUDLFT Registration') != -1

    def test_withdraw_club_points_if_pusrchese_places(self, client, clubs, competitions):
        post_data = {
            'club': clubs.clubs[0]['name'],
            'competition': competitions.competitions[0]['name'],
            'places': '15'
        }
        club_points = clubs.get_club_by_name(post_data['club'])['points']

        res = client.post('/purchasePlaces', data=post_data, follow_redirects=True)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find("<title>Summary | GUDLFT Registration</title>") != -1
        assert data.find(f"Points available: {str(int(club_points) - int(post_data['places']))}") != -1

    def test_purchase_places_greater_than_club_points(self, client, clubs, competitions):
        post_data = {
            'club': clubs.clubs[0]['name'],
            'competition': competitions.competitions[0]['name'],
            'places': '21'
        }

        res = client.post('/purchasePlaces', data=post_data, follow_redirects=True)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find("<title>Summary | GUDLFT Registration</title>") != -1
        assert data.find('<li>You cannot reserve more place than your number of points</li>') != -1
        assert data.find('Points available: 20') != -1
