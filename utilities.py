import json


CLUBS_FILE = "clubs.json"
COMPETITIONS_FILE = "competitions.json"


class Competitions:
    def __init__(self) -> None:
        with open(COMPETITIONS_FILE) as file:
            self.competitions = json.load(file)['competitions']

    def get_list(self) -> list[dict]:
        return self.competitions

    def get_competition(self, competition_name: str) -> dict:
        competition = [
            competition for competition in self.competitions if competition['name'] == competition_name
        ]
        if competition:
            return competition[0]

    def get_competition_place(self, competition_name: str) -> int:
        competition = self.get_competition(competition_name)
        if competition:
            return competition['numberOfPlaces']

    def withdraw_competition_places(self, competition_name: str, nb_of_place: int) -> None:
        competition = self.get_competition(competition_name)
        if competition:
            competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - nb_of_place)


class Clubs:
    def __init__(self) -> None:
        with open(CLUBS_FILE) as file:
            self.clubs = json.load(file)['clubs']

    def get_list(self) -> list[dict]:
        return self.clubs

    def get_club_by_email(self, email: str) -> dict:
        club = [
            club for club in self.clubs if club['email'] == email
        ]
        if club:
            return club[0]

    def get_club_by_name(self, name: str) -> dict:
        club = [
            club for club in self.clubs if club['name'] == name
        ]
        if club:
            return club[0]

    def get_club_points(self, club_name: str) -> dict:
        club = self.get_club(club_name)
        if club:
            return club['points']

    def withdraw_club_points(self, club_name: str, points: int) -> None:
        club = self.get_club(club_name)
        if club:
            club['points'] = str(int(club['points']) - points)
