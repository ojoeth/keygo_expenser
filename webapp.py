import flask, datetime, sqlite3, getjourneys, cli
app = flask.Flask(__name__)

@app.route("/")
def hello_world():
    journeydata=getjourneys(2023, 5, "testuser", "testpass")
    journeys = []
    for t in journeydata:
        for transaction in t["transactions"]:
            for ticket in transaction["journeyPattern"]["tickets"]:
                # Filter by station if specified in args
                if 'filter' in globals():
                    if ticket["destinationName"] == filter:
                        price = cli.convertFare(ticket["fare"])
                        totalcost = totalcost + price
                        journeys.append(t["date"], (ticket["originName"] + " to " +  ticket["destinationName"]), ticket["description"].title(), ("£%.2f"%price))
                else:
                    price = cli.convertFare(ticket["fare"])
                    totalcost = totalcost + price
                    journeys.append(t["date"], (ticket["originName"] + " to " +  ticket["destinationName"]), ticket["description"].title(), ("£%.2f"%price))

    return flask.render_template('main.html', journeys=journeys)



if __name__ == "__main__":
    app.run(host='0.0.0.0')