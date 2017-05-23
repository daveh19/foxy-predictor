from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Party, Polling, Projection, Growth, Election, Popularity
import wahlrecht_polling_firms

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
        return getPollingData()
    elif request.method == 'POST':
        tables = wahlrecht_polling_firms.get_tables()
        firms = []
        for k,v in tables.items():
            # get all columns from each table
            heads = v.columns
            # access columns data by subscript
            print(v[heads[0]])
            print(v[heads[1]])
            firms.append(loadPollingData(k))
        return str(firms)

# Parties app.route() decorator
@app.route("/parties/", methods=['GET', 'POST'])
def partiesFunction():
    if request.method == 'GET':
        return getAllParties()

# Growth app.route() decorator
@app.route("/growth", methods=['GET'])
def growthFunction():
    if request.method == 'GET':
        return getGrowth()

# Get parties data
def getAllParties():
    all_parties = session.query(Party).all()
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
    app.run(host='0.0.0.0', port=5000)
