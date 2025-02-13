import datetime

import pytest
from unittest.mock import MagicMock

from server import create_app


def upper_str_date():
    upper_date = datetime.datetime.now() + datetime.timedelta(days=2)
    return upper_date.strftime("%Y-%m-%d %H:%M:%S")


@pytest.fixture
def clubs():
    club = {
        "name": "test_club_name",
        "email": "test@test.com",
        "points": "20"
    }
    mock_clubs = MagicMock()

    mock_clubs.get_list.return_value = [club]
    mock_clubs.get_club_by_name.return_value = club
    mock_clubs.get_club_by_email.return_value = club
    mock_clubs.withdraw_club_point.return_value = None
    return mock_clubs


@pytest.fixture
def competitions():
    competition = {
        "name": "test_competition_name",
        "date": upper_str_date(),
        "numberOfPlaces": "20"
    }
    mock_competitions = MagicMock()

    mock_competitions.get_list.return_value = [competition]
    mock_competitions.get_competition.return_value = competition
    mock_competitions.withdraw_competition_places.return_value = None
    return mock_competitions


@pytest.fixture
def client(clubs, competitions):
    app = create_app(clubs, competitions)
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


class TestUnitServer:

    def test_index_route_is_accessible(self, client):
        res = client.get('/')
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<title>GUDLFT Registration</title>') != -1

    def test_login_with_valid_email(self, client):
        credential = {
            'email': 'test@test.com'
        }

        res = client.post('/showSummary', data=credential)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find("<h2>Welcome, test@test.com </h2>") != -1
        assert data.find("test_competition_name<br />") != -1

    def test_login_with_invalid_email(self, client, clubs):
        clubs.get_club_by_email.return_value = None
        credential = {
            'email': 'bad@email.com'
        }

        res = client.post('/showSummary', data=credential)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<li>Email not found</li>') != -1
        assert data.find('<title>GUDLFT Registration</title>') != -1

    def test_logout_user(self, client):
        res = client.get('/logout', follow_redirects=True)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<title>GUDLFT Registration</title>') != -1

    def test_book_reservation_with_valid_club_and_competition(self, client):
        competition = 'test_competition_name'
        club = 'test_club_name'

        res = client.get(f'/book/{competition}/{club}')
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find(f'<title>Booking for {competition} || GUDLFT</title>') != -1

    def test_book_reservation_with_invalid_club_or_competition(self, client, clubs):
        clubs.get_club_by_name.return_value = None

        res = client.get('/book/invalid_competition/invalid_club', follow_redirects=True)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<li>Something went wrong-please try again</li>') != -1
        assert data.find('<title>GUDLFT Registration</title>') != -1

    def test_purchase_place_with_valid_club_and_competition(self, client):
        post_data = {
            'club': 'test_club_name',
            'competition': 'test_competition_name',
            'places': '10'
        }

        res = client.post('/purchasePlaces', data=post_data, follow_redirects=True)
        data = res.data.decode()
        assert res.status_code == 200
        assert data.find('<title>Summary | GUDLFT Registration</title>') != -1

    def test_purchase_place_with_invalid_club_and_competition(self, client, clubs):
        clubs.get_club_by_name.return_value = None
        post_data = {
            'club': 'invalid_club_name',
            'competition': 'invalid_competition_name',
            'places': '10'
        }

        res = client.post('/purchasePlaces', data=post_data, follow_redirects=True)
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<title>GUDLFT Registration</title>') != -1

    def test_club_balance_page(self, client):
        res = client.get('/clubsBalance')
        data = res.data.decode()

        assert res.status_code == 200
        assert data.find('<title>GUDLFT Clubs points balance</title>') != -1
        assert data.find('<td>test_club_name</td>') != -1
        assert data.find('<td>20</td>') != -1
