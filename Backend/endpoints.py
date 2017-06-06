from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Party, Polling, Projection, Growth, Election, Popularity
import wahlrecht_polling_firms
from extract_data import Source

# Create an engine with the database specified
engine = create_engine('sqlite:///polls.db')
Base.metadata.bind = engine

# Create a session for your engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Declare app
app = Flask(__name__)

# Initial app.route() decorator
@app.route("/")

# Polling app.route() decorator
@app.route("/parties/polls", methods=['GET', 'POST'])
def pollingFunction():
    if request.method == 'GET':
        print("--- GETPOLLINGDATA ---")
        return getPollingData()

    elif request.method == 'POST':
        print("--- POSTPOLLINGDATA ---")

        tables_per_firms = wahlrecht_polling_firms.get_tables()
        #with extract_data:
        source_per_firms = Source('wahlrecht')
        tables_per_firms = source_per_firms.get_tables()

        firms = []
        for k, df in tables_per_firms.items():
            # get all columns from each table
            heads = df.columns
            print(heads)
            # access columns data by subscript
            date = df[heads]["Datum"]
            people_asked = df[heads]["Befragte"]
            # get first and last party to loop through
            first_party = heads.get_loc("CDU/CSU")
            last_party = heads.get_loc("Sonstige") + 1
            party_keys = heads[first_party:last_party]
            parties = {}
            for p in party_keys:
                parties[p] = df[p]

            for party, values in parties.items():
                for percentage in values:
                    try:
                        percentage = float(percentage.replace('%', '').replace(',', '.').strip())
                    except ValueError:
                        print("Error")
                    print(percentage)


            firms.append(loadPollingData(k))
        return str(firms)


# Parties app.route() decoratorCDU_CSU	SPD	GRÜNE	FDP	LINKE	AfD	Sonstige
@app.route("/parties/", methods=['GET', 'POST'])
def partiesFunction():
    if request.method == 'GET':
        print("--- GETPARTIES ---")

        return getAllParties()

# Growth app.route() decorator
@app.route("/growth", methods=['GET'])
def growthFunction():
    print("--- GETGROWTH ---")

    if request.method == 'GET':
        return getGrowth()

# Get parties data
def getAllParties():
    all_parties = session.query(Party).all()
    print(all_parties)
    parties = []
    for party in all_parties:
        popularity = []
        election = []
        party_rows = session.query(Popularity).filter(party.id == Popularity.party_id).all()
        for p in party_rows:
            popularity.append({
                "state_name" : p.state_name,
                "percentage" : p.percentage
            })
        election_rows = session.query(Election).filter(party.id == Election.party_id).all()
        for e in election_rows:
            election.append({
                "year" : e.year,
                "percentage" : e.percentage
            })
        parties.append({
            "name" : party.name,
            "leader": party.leader,
            "abbreviation": party.abbreviation,
            "popularity": popularity,
            "past_election": election
        })
    print(parties)
    return jsonify(parties)

# Get growth data
def getGrowth():
    growths = session.query(Growth).all()
    return jsonify(Growth=[g.serialize for g in growths])

# Get polling data
def getPollingData():
    polling = session.query(Polling).all()
    firms = []
    for firm in polling:
        parties = []
        party_rows = session.query(Projection).filter(firm.id == Projection.polling_id).all()
        for party in party_rows:
            parties.append({
                "party_name" : party.party_name,
                "percentage" : party.percentage,
                "date" : party.date,
                "people" : party.people
            })
        firms.append({
            'firm': firm.firm_name,
            'parties': parties
        })

    return jsonify(firms)

# Load polling data
def loadPollingData(k):
    #print(k)
    projection = Projection()
    return k



# Run app
if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
