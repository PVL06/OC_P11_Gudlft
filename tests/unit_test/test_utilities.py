import pytest

from utilities import Competitions, Clubs


@pytest.fixture
def competitions():
    sut = Competitions()
    sut.competitions = [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        }
    ]
    return sut


@pytest.fixture
def clubs():
    sut = Clubs()
    sut.clubs = [
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        }
    ]
    return sut


class TestCompetitions:

    def test_get_competitions_list(self, competitions):
        assert len(competitions.get_list()) == 1

    def test_get_competition_and_place_with_valid_name(self, competitions):
        name = 'Spring Festival'
        assert competitions.get_competition(name) == competitions.competitions[0]
        assert competitions.get_competition_place(name) == "25"

    def test_get_competition_and_place_with_invalid_name(self, competitions):
        name = 'Fall Classic'
        assert competitions.get_competition(name) is None
        assert competitions.get_competition_place(name) is None

    def test_withdraw_place_with_valid_name(self, competitions):
        name = 'Spring Festival'
        competitions.withdraw_competition_places(name, 5)
        assert competitions.competitions[0]['numberOfPlaces'] == "20"

    def test_withdraw_place_with_invalid_name(self, competitions):
        name = 'Fall Classic'
        competitions.withdraw_competition_places(name, 5)
        assert competitions.competitions[0]['numberOfPlaces'] == "25"


class TestClubs:

    def test_get_clubs_list(self, clubs):
        assert len(clubs.get_list()) == 1

    def test_connection_and_points_with_good_email_or_name(self, clubs):
        email = 'admin@irontemple.com'
        name = 'Iron Temple'
        assert clubs.get_club_by_email(email) == clubs.clubs[0]
        assert clubs.get_club_by_name(name) == clubs.clubs[0]
        assert clubs.get_club_points(name) == clubs.clubs[0]['points']

    def test_connection_and_points_with_bad_email_or_name(self, clubs):
        email = 'bad@email.com'
        name = 'bad name'
        assert clubs.get_club_by_email(email) is None
        assert clubs.get_club_by_name(name) is None
        assert clubs.get_club_points(name) is None

    def test_withdraw_club_point_with_good_name(self, clubs):
        name = 'Iron Temple'
        clubs.withdraw_club_points(name, 4)
        assert clubs.clubs[0]['points'] == '0'

    def test_withdraw_club_point_with_bad_name(self, clubs):
        name = 'bad name'
        clubs.withdraw_club_points(name, 4)
        assert clubs.clubs[0]['points'] == '4'
