from playwright.sync_api import Page, expect

LOCAL_HOST = "http://127.0.0.1:5000"

club = {
    "name": "Hurricane's",
    "email": "hurricanesgym@example.com",
    "points": "5"
}

def _index(page: Page):
    page.goto(f"{LOCAL_HOST}/")
    expect(page).to_have_title("GUDLFT Registration")

def _login(page: Page, email: str):
    page.get_by_role("textbox").fill(email)
    page.get_by_role("button", name="Enter").click()
    expect(page).to_have_title("Summary | GUDLFT Registration")

def test_booking_place(page: Page):
    _index(page)
    _login(page, club['email'])
    expect(page.get_by_text(f"Points available: {club['points']}")).to_be_visible()
    expect(page.get_by_role("listitem")).to_have_count(10)

    items = page.get_by_role("listitem").all()
    valid_competition_url = items[4].get_by_role("link").get_attribute("href")
    page.goto(f"{LOCAL_HOST}" + valid_competition_url)
    expect(page).to_have_title("Booking for Iron Warriors Challenge || GUDLFT")

    page.get_by_role("spinbutton").fill('1')
    page.get_by_role("button", name="book").click()
    expect(page).to_have_title("Summary | GUDLFT Registration")
    expect(page.get_by_text("Great-booking complete!")).to_be_visible()
    expect(page.get_by_text(f"Points available: {str(int(club['points']) - 1)}")).to_be_visible()
    expect(page.get_by_text("Number of Places: 19")).to_be_visible()

    

def test_logout(page: Page):
    _index(page)
    _login(page, club['email'])

    page.get_by_role("link", name="logout").click()
    expect(page).to_have_title("GUDLFT Registration")

def test_clubs_points_array_page(page: Page):
    _index(page)
    array_url = page.get_by_role('link').get_attribute("href")
    page.goto(f"{LOCAL_HOST}{array_url}")
    expect(page).to_have_title("GUDLFT Clubs points balance")

def test_login_with_invalid_email(page: Page):
    _index(page)
    page.get_by_role("textbox").fill("bad@email.com")
    page.get_by_role("button", name="Enter").click()
    expect(page).to_have_title("GUDLFT Registration")
    expect(page.get_by_text("Email not found")).to_be_visible()