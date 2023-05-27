import getjourneys, getpass, datetime, sys

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

def convertFare(fare):
    if fare == 0:
        price = 0
    else:
        price = (fare/100) # Avoid dividing by zero!! 
    return price

def runcli():
    if len(sys.argv) < 3:
        print("Please provide the year and month as arguments when calling this script. Example: 2023 02")
        exit(1)

    year = int(sys.argv[1])
    month = int(sys.argv[2])

    if len(sys.argv) == 4:
        filter = sys.argv[3]
        journeydata = getjourneys.grabJourneys(2023, 5, input("Username: "), getpass.getpass())
        htmlfilename = (datetime.datetime.now().isoformat() + ".html")
        f = open(htmlfilename, 'w')
        f.write("""<link href='https://fonts.googleapis.com/css?family=Rationale' rel='stylesheet'>
        <link href='style.css' rel='stylesheet'>
        <div style="background-color:#fff; padding-left:10px; padding-top: 10px; height: 600px">
        """)
        totalcost = 0

        for t in journeydata:
            for transaction in t["transactions"]:
                for ticket in transaction["journeyPattern"]["tickets"]:
                    # Filter by station if specified in args
                    if 'filter' in globals():
                        if ticket["destinationName"] == filter:
                            price = convertFare(ticket["fare"])
                            totalcost = totalcost + price
                            print(t["date"], (ticket["originName"] + " to " +  ticket["destinationName"]), ticket["description"].title(), ("£%.2f"%price))
                            f.write(formulateHTML(ticket["description"].title(), ticket["destinationName"], ticket["originName"], ("£%.2f"%price), t["date"]))
                    else:
                        price = convertFare(ticket["fare"])
                        totalcost = totalcost + price
                        print(t["date"], (ticket["originName"] + " to " +  ticket["destinationName"]), ticket["description"].title(), ("£%.2f"%price))
                        f.write(formulateHTML(ticket["description"].title(), ticket["destinationName"], ticket["originName"], ("£%.2f"%price), t["date"]))

        f.write("</div>")
        f.write("<br> Total: " + ("£%.2f"%totalcost))
        f.close()

runcli()