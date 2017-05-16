from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Party

# Create an engine with the database specified
engine = create_engine('sqlite:///polls.db')
Base.metadata.bind = engine

# Create a session for your engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


# Create the appropriate app.route functions,
#test and see if they work


#app.route() decorator here
@app.route("/")

#Another decorator which defines parties endpoint
@app.route("/parties/", methods = ['GET', 'POST'])
def partiesFunction():
  if request.method == 'GET':
    #Call the method to Get all of the parties
    return getAllParties()

  elif request.method == 'POST':
    #Call the method to create a new party

    name = request.args.get('name', '')
    abbreviation = request.args.get('abbreviation', '')
    leader = request.args.get('leader', '')
    alliance = request.args.get('alliance', '')
    return createANewParty(name, abbreviation, leader, alliance)

#Another app.route() which gets details for a specific party
@app.route("/parties/<int:id>", methods = ['GET'])
#Call the method to view a specific party
def partiesFunctionId(id):
  if request.method == 'GET':
    return getParty(id)

#Another app.route() which gets all the projections
@app.route("/parties/projection/", methods = ['GET'])
#Call the method to view prjojections for all parties
def partiesFunctionProjection():
  if request.method == 'GET':
    return getPartyProjections()

#Another app.route() which gets all the projections
@app.route("/parties/popularity/", methods = ['GET'])
#Call the method to view prjojections for all parties
def partiesFunctionPopularity():
  if request.method == 'GET':
    return getPartyPopularity()

# Get all parties in a list
def getAllParties():
  parties = session.query(Party).all()
  return jsonify(Parties=[i.serialize for i in parties])

# Create a new party
def createANewParty(name, abbreviation, leader, alliance):
  party = Party(name = name, abbreviation = abbreviation, leader = leader, alliance = alliance)
  session.add(party)
  session.commit()
  return jsonify(Party=party.serialize)

# Get a specific party
def getParty(id):
  party = session.query(Party).filter_by(id = id).one()
  return jsonify(party=party.serialize)

# Get all party projections
def getPartyProjections():
  projections = session.query(Projection).all()
  return jsonify(Projections=[i.serialize for i in projections])

 # Get all party projections
 def getPartyPopularity():
     popularities = session.query(Popularity).all()
     return jsonify(Popularities=[i.serialize for i in popularities])

if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
