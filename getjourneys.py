import requests, json, datetime, calendar

# Define auth class
class auth:
    auth = ["username", "password"]
    headers = {}
    request = requests.post
    data = {}

class journey:
    headers = {}
    request = requests.post
    data = {}




def grabJourneys(year, month, username, password):
    session = requests.session() # create session with requests

    monthbegin = datetime.datetime(year, month, 1)
    monthend = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
    url = ("https://api.southernrailway.com/smartcard/31999362/keygo/journey-history?startDate=" + monthbegin.isoformat() + "Z&endDate=" + monthend.isoformat() + "Z")
    auth.auth = [username, password]
    auth.headers = {"x-access-token" : "otrl|a6af56be1691ac2929898c9f68c4b49a0a2d930849770dba976be5d792a", "Content-Type" : "application/json"} # Hardcoded access token thing is always the same
    auth.request = session.post("https://api.southernrailway.com/customers/auth", headers=auth.headers, json={"username":auth.auth[0], "password" : auth.auth[1], "grant_type" : "password", "session_short" : True})
    auth.data = json.loads(auth.request.content.decode("ascii"))

    journey.headers = auth.headers.copy()
    journey.headers.update({"user-role" : "CUSTOMER", "user-id" : str(auth.data["links"][auth.data["result"]["customer"]]["id"]), "x-customer-token" : str(auth.data["result"]["accessToken"])})
    journey.request = session.get(url, headers=journey.headers)
    journey.data = json.loads(journey.request.content.decode("ascii"))


    # Sign out
    session.delete(("https://api.southernrailway.com/customers/auth/" + str(auth.data["result"]["accessToken"])), headers=auth.headers)

    return journey.data["dailyTransactions"]



