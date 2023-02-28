import requests, json, datetime, calendar, sys, getpass

session = requests.session() # create session with requests

if len(sys.argv) < 3:
    print("Please provide the year and month as arguments when calling this script. Example: 2023 02")
    exit(1)

year = int(sys.argv[1])
month = int(sys.argv[2])

if len(sys.argv) == 4:
    filter = sys.argv[3]

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

auth.auth = [input("Username: "), getpass.getpass()]
auth.headers = {"x-access-token" : "otrl|a6af56be1691ac2929898c9f68c4b49a0a2d930849770dba976be5d792a", "Content-Type" : "application/json"} # Hardcoded access token thing is always the same
auth.request = session.post("https://api.southernrailway.com/customers/auth", headers=auth.headers, json={"username":auth.auth[0], "password" : auth.auth[1], "grant_type" : "password", "session_short" : True})
auth.data = json.loads(auth.request.content.decode("ascii"))

name = (auth.data["links"][auth.data["result"]["customer"]]["firstNames"] + " " + auth.data["links"][auth.data["result"]["customer"]]["surname"])

monthbegin = datetime.datetime(year, month, 1)
monthend = datetime.datetime(year, month, calendar.monthrange(year, month)[1], 23, 59, 59)
url = ("https://api.southernrailway.com/smartcard/31999362/keygo/journey-history?startDate=" + monthbegin.isoformat() + "Z&endDate=" + monthend.isoformat() + "Z")

journey.headers = auth.headers.copy()
journey.headers.update({"user-role" : "CUSTOMER", "user-id" : str(auth.data["links"][auth.data["result"]["customer"]]["id"]), "x-customer-token" : str(auth.data["result"]["accessToken"])})
journey.request = session.get(url, headers=journey.headers)
journey.data = json.loads(journey.request.content.decode("ascii"))


# Sign out
session.delete(("https://api.southernrailway.com/customers/auth/" + str(auth.data["result"]["accessToken"])), headers=auth.headers)


# Print data
print("Welcome", name)

def formulateHTML(type, dst, src, price, date):
    tickethtml = ("""
     <div class="ticketOrange">
         <div class="ticketCream">
             <div class="standardTicket">
    """ 
    + date + "<br>\n" + type + "<br>\n" + src + " to " + dst + "<br>\n" + price + 
    """
             </div>
         </div>
     </div>
    """)
    return tickethtml

def convertFare(ticket):
    if ticket["fare"] == 0:
        price = 0
    else:
        print(ticket["fare"]/100)
        price = (ticket["fare"]/100) # Avoid dividing by zero!! 
    return price


htmlfilename = (datetime.datetime.now().isoformat() + ".html")
f = open(htmlfilename, 'w')
f.write("""<link href='https://fonts.googleapis.com/css?family=Rationale' rel='stylesheet'>
<link href='style.css' rel='stylesheet'>
<div style="background-color:#fff; padding-left:10px; padding-top: 10px; height: 600px">
""")
totalcost = 0
for t in journey.data["dailyTransactions"]:
    for transaction in t["transactions"]:
        for ticket in transaction["journeyPattern"]["tickets"]:
            # Filter by station if specified in args
            if 'filter' in globals():
                if ticket["destinationName"] == filter:
                    price = convertFare(ticket)
                    totalcost = totalcost + price
                    print(t["date"], (ticket["originName"] + " to " +  ticket["destinationName"]), ticket["description"].title(), ("£%.2f"%price))
                    f.write(formulateHTML(ticket["description"].title(), ticket["destinationName"], ticket["originName"], ("£%.2f"%price), t["date"]))
            else:
                price = convertFare(ticket)
                totalcost = totalcost + price
                print(t["date"], (ticket["originName"] + " to " +  ticket["destinationName"]), ticket["description"].title(), ("£%.2f"%price))
                f.write(formulateHTML(ticket["description"].title(), ticket["destinationName"], ticket["originName"], ("£%.2f"%price), t["date"]))

f.write("</div>")
f.write("Total: " + ("£%.2f"%totalcost))
f.close()

