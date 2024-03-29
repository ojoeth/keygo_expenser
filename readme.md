# KeyGo Expenser
This script is something I threw together while reverse engineering the Southern Rail [KeyGo](https://www.southernrailway.com/tickets/the-key-smartcard/keygo) API.

The idea is that you input a year, month, and optionally a destination station to filter results, then log in to Southern's API using the prompt, and it will spit out a crude HTML file with some CSS train tickets containing information about your journeys, possibly allowing you to make expensing train travel a little easier.

## Usage

### CLI
- Run `cli.py` with `year`, `month`. Optionally, provide a `station` to filter results for journeys to a specific station.

`python3 cli.py 2023 05 Lewes`

### Web

#### Docker
- `git clone https://github.com/ojoeth/keygo_expenser`
- `docker build -t keygo .`
- `docker run --name=keygo -p 8000:8000 -dt keygo`
- Navigate to http://localhost:8000 in your browser
- Optionally, configure a reverse proxy to handle HTTPS

#### Manually
- Ensure Flask is installed
- Run flask on webapp.py

`flask --app webapp.py run`
- Navigate to http://localhost:5000 in your browser