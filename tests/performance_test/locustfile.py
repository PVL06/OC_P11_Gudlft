from locust import HttpUser, task


class ServerPerfTest(HttpUser):

    @task(10)
    def index(self):
        self.client.get("/")

    @task(10)
    def club_balance(self):
        self.client.get("/clubsBalance")

    @task(2)
    def login(self):
        self.client.post(
            "/showSummary",
            {"email": "thundersbluff@example.com"}
        )

    @task(2)
    def booking(self):
        competition = "Strongman Classic"
        club = "Vanguard Strength"
        self.client.get(f"/book/{competition}/{club}")

    @task(1)
    def purchase_places(self):
        club = "Vanguard Strength"
        competition = "Strongman Classic"
        places = "1"
        self.client.post(
            "/purchasePlaces",
            {
                "club": club,
                "competition": competition,
                "places": places
            }
        )

    @task(2)
    def logout(self):
        self.client.get("/logout")
