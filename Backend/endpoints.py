from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Party, Polling, Projection, Growth, Election, Popularity
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
        return loadPollingData()


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
    return jsonify(parties)

# Get growth data
def getGrowth():
    growths = session.query(Growth).all()
    return jsonify(Growth=[g.serialize() for g in growths])

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
                "people" : party.people,
                "region" : party.region
            })
        firms.append({
            'firm': firm.firm_name,
            'parties': parties
        })

    return jsonify(firms)

# Load polling data
def loadPollingData():
    #tables_per_firms = wahlrecht_polling_firms.get_tables()
    # extract data from wahlrecht source
    source_wahlrecht = Source('wahlrecht_country')
    tables_wahlrecht = source_wahlrecht.get_tables()

    dict_polling = {}
    polling = session.query(Polling).all()
    dict_polling = {p.firm_name: p.id for p in polling}

    for k, df in tables_wahlrecht.items():
        percentages = []
        datum = df['Datum']
        befragte = df['Befragte']
        parties = df.columns
        for p in df.columns:
            if p !='Datum' and p!='Befragte':
                percentages = df[p]
                if len(percentages) > 0:
                     for i in range(len(percentages)):
                         projection = Projection(party_name = p, percentage = percentages[i], date = datum[i], people = befragte[i], region = "germany", polling_id = dict_polling[k])
                         session.add(projection)
                         session.commit()
    # del source_wahlrecht

    # source_wahlrecht = Source('wahlrecht_states')
    # tables_wahlrecht = source_wahlrecht.get_tables()
    #
    #
    # def convertInstitue(ins):
    #     ins = ins.lower()
    #     if ins == 'ForschungsgruppeWahlen'.lower():
    #         ins = 'politbarometer'
    #     elif ins == 'Infratestdimap'.lower() or 'Infratest'.lower():
    #         ins = 'dimap'
    #     return ins
    #
    # for state, df in tables_wahlrecht.items():
    #     datum = df['Datum']
    #     befragte = df['Befragte']
    #     ins_series = df['Institut']
    #     ins = [i.strip() for i in ins_series.to_string(index=False).split('\n')]
    #     percentages = []
    #     # print(ins)
    #     # print()
    #     # print(df.columns)
    #     for firm in ins:
    #         firm = convertInstitue(firm)
    #         for ind, p in enumerate(df.columns):
    #             if len(ins_series) != 0:
    #                 if p !='Datum' and p!='Befragte' and p!= 'Auftrag-geber' and p!='Institut':
    #                     # print(state,' ', firm, ' ', p)
    #                     percentages = df[p]
    #                     if len(percentages) > 0:
    #                          for i in range(len(percentages)):
    #                              projection = Projection(party_name = p, percentage = percentages[i], date = datum[i], people = befragte[i], region = state, polling_id = dict_polling[firm])
    #                              session.add(projection)
    #                              session.commit()
    return "Added new polling data"

# Run app
if __name__ == '__main__':
    app.debug = False
    app.run(host='localhost', port=5000)
