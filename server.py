from flask import Flask, render_template, request, redirect, flash, url_for

from utilities import Clubs, Competitions


def create_app(clubs, competitions):

    app = Flask(__name__)
    app.secret_key = 'something_special'

    @app.route('/')
    def index():
        return render_template('index.html')

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
            flash("Email not found")
            return render_template('index.html')

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        found_club = clubs.get_club_by_name(club)
        found_competition = competitions.get_competition(competition)

        if found_club and found_competition:
            return render_template(
                'booking.html',
                club=found_club,
                competition=found_competition
            )
        else:
            flash("Something went wrong-please try again")
            return redirect(url_for('index'))

    @app.route('/purchasePlaces', methods=['POST'])
    def purchase_places():
        places_required = int(request.form['places'])
        club = clubs.get_club_by_name(request.form['club'])
        competition = competitions.get_competition(request.form['competition'])

        if club and competition:
            if places_required > int(club['points']):
                flash("You cannot reserve more place than your number of points")
            elif places_required > 12:
                flash('You cannot reserve more than 12 places')
            else:
                competitions.withdraw_competition_places(
                    competition,
                    places_required
                )
                clubs.withdraw_club_points(
                    club,
                    places_required
                )

                flash('Great-booking complete!')

            return render_template(
                'welcome.html',
                club=club,
                competitions=competitions.get_list()
            )
        else:
            flash('Something went wrong-please try again')
            return redirect(url_for('index'))

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


if __name__ == '__main__':
    clubs = Clubs()
    competitions = Competitions()
    app = create_app(clubs, competitions)
    app.run(debug=True)
