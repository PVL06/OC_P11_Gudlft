from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime

from utilities import Clubs, Competitions

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def create_app(clubs, competitions):

    app = Flask(__name__)
    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/clubsBalance')
    def clubs_balance():
        return render_template(
            'balance.html',
            clubs=clubs.get_list())

    @app.route('/showSummary', methods=['POST'])
    def show_summary():
        club = clubs.get_club_by_email(request.form['email'])
        if club:
            return render_template(
                'welcome.html',
                club=club,
                competitions=competitions.get_list()
            )
        else:
            flash("Email not found", "error")
            return redirect(url_for('index'))

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        found_club = clubs.get_club_by_name(club)
        found_competition = competitions.get_competition(competition)

        if found_club and found_competition:
            competition_date = datetime.strptime(
                found_competition['date'],
                DATE_FORMAT
            )

            if competition_date > datetime.now():
                return render_template(
                    'booking.html',
                    club=found_club,
                    competition=found_competition
                )
            else:
                flash(f"{found_competition['name']} competition is over", "error")
                return render_template(
                    'welcome.html',
                    club=found_club,
                    competitions=competitions.get_list()
                )
        else:
            flash("Something went wrong-please try again", "error")
            return redirect(url_for('index'))

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        places_required = int(request.form['places'])
        club = clubs.get_club_by_name(request.form['club'])
        competition = competitions.get_competition(request.form['competition'])

        if club and competition:
            if places_required > int(club['points']):
                flash("You cannot reserve more place than your number of points", "error")
            elif places_required > 12:
                flash('You cannot reserve more than 12 places', "error")
            elif places_required > int(competition['numberOfPlaces']):
                flash("You cannot reserve more space than available", "error")
            else:
                competitions.withdraw_competition_places(
                    competition,
                    places_required
                )
                clubs.withdraw_club_points(
                    club,
                    places_required
                )

                flash('Great-booking complete!', 'done')

            return render_template(
                'welcome.html',
                club=club,
                competitions=competitions.get_list()
            )
        else:
            flash('Something went wrong-please try again', "error")
            return redirect(url_for('index'))

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    clubs = Clubs()
    competitions = Competitions()
    app = create_app(clubs, competitions)
    app.run(debug=True)
