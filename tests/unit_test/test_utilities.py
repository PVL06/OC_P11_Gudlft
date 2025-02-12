import pytest

from utilities import Competitions, Clubs


@pytest.fixture
def competitions():
    sut = Competitions()
    sut.competitions = [
        {
            "name": "good_competition_name",
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
            "name": "good_club_name",
            "email": "good@test.com",
            "points": "4"
        }
    ]
    return sut


class TestCompetitions:

    def test_get_competitions_list(self, competitions):
        assert len(competitions.get_list()) == 1

    def test_get_competition_and_place_with_valid_name(self, competitions):
        name = 'good_competition_name'
        competition = competitions.get_competition(name)

        assert competition == competitions.competitions[0]
        assert competition['numberOfPlaces'] == "25"

    def test_get_competition_with_invalid_name(self, competitions):
        name = 'bad_competition_name'
        competition = competitions.get_competition(name)

        assert competition is None

    def test_withdraw_place_with_valid_name(self, competitions):
        name = 'good_competition_name'
        competition = competitions.get_competition(name)
        competitions.withdraw_competition_places(competition, 5)

        assert competitions.competitions[0]['numberOfPlaces'] == "20"

    def test_withdraw_place_with_invalid_name(self, competitions):
        name = 'bad_competition_name'
        competition = competitions.get_competition(name)
        competitions.withdraw_competition_places(competition, 5)

        assert competitions.competitions[0]['numberOfPlaces'] == "25"


class TestClubs:

    def test_get_clubs_list(self, clubs):
        assert len(clubs.get_list()) == 1

    def test_connection_with_good_email_or_name(self, clubs):
        email = 'good@test.com'
        name = 'good_club_name'
        club_email = clubs.get_club_by_email(email)
        club_name = clubs.get_club_by_name(name)

        assert club_email == clubs.clubs[0]
        assert club_name == clubs.clubs[0]

    def test_connection_with_bad_email_or_name(self, clubs):
        email = 'bad@email.com'
        name = 'bad_club_name'

        club_email = clubs.get_club_by_email(email)
        club_name = clubs.get_club_by_name(name)

        assert club_email is None
        assert club_name is None

    def test_withdraw_club_point_with_good_name(self, clubs):
        name = 'good_club_name'
        club = clubs.get_club_by_name(name)
        clubs.withdraw_club_points(club, 4)

        assert club['points'] == '0'

    def test_withdraw_club_point_with_bad_name(self, clubs):
        name = 'bad_club_name'
        club = clubs.get_club_by_name(name)
        clubs.withdraw_club_points(club, 4)

        assert clubs.clubs[0]['points'] == '4'
