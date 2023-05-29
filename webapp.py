import flask, datetime, sqlite3, getjourneys, cli
app = flask.Flask(__name__)


@app.route("/")
def login():

    return flask.render_template('login.html', current_month=datetime.datetime.today().strftime("%Y-%m"))

@app.route("/journeys", methods=['POST'])
def show_journey_page():
    year, month=flask.request.form["month"].split("-")
    journeydata=getjourneys.grabJourneys(int(year), int(month), flask.request.form["username"], flask.request.form["password"])
    journeys = []
    totalcost=0
    for t in journeydata:
        for transaction in t["transactions"]:
            for ticket in transaction["journeyPattern"]["tickets"]:
                # Filter by station if specified in args
                if 'filter' in globals():
                    if ticket["destinationName"] == filter:
                        price = cli.convertFare(ticket["fare"])
                        totalcost = totalcost + price
                        journeys.append(str(t["date"]) + "\n" + (ticket["originName"] + " to " +  ticket["destinationName"]) + str(ticket["description"].title()) + "\n" + str(("£%.2f"%price)))
                else:
                    price = cli.convertFare(ticket["fare"])
                    totalcost = totalcost + price
                    journeys.append(str(t["date"]) + "\n" + (ticket["originName"] + " to " +  ticket["destinationName"]) + str(ticket["description"].title()) + "\n" + str(("£%.2f"%price)))

    return flask.render_template('main.html', journeys=journeys, total=totalcost)



if __name__ == "__main__":
    app.run(host='0.0.0.0')