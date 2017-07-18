"""
Module containing the table classes for the database.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, create_engine, Float, func, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker

# Base Declaration
Base = declarative_base()

# Party Class
class Party(Base):
    __tablename__ = 'party'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    leader = Column(String(80), nullable=False)
    abbreviation = Column(String(80), nullable=False)
    elections = relationship('Election', backref = 'party', lazy='dynamic')

    def serialize(self):
        return {
        "party_name" : self.party_name,
        "leader": self.leader,
        "abbreviation": self.abbreviation
        }

# Polling Class
class Polling(Base):
    __tablename__ = 'polling'
    id = Column(Integer, primary_key=True)
    firm_name = Column(String(80), nullable=False)
    projections = relationship('Projection', backref = 'polling', lazy='dynamic')

    def serialize(self):
        return {
        "firm_name" : self.firm_name
        }


# Projection Class
class Projection(Base):
    __tablename__ = 'projection'
    id = Column(Integer, primary_key=True)
    party_name = Column(String(80))
    percentage = Column(Integer)
    date = Column(String(80))
    people = Column(String(80))
    region = Column(String(80))
    polling_id = Column(Integer, ForeignKey('polling.id'))

    def serialize(self):
        return {
        "party_name" : self.party_name,
        "percentage" : self.percentage,
        "date" : self.date,
        "people" : self.people,
        "region" : self.region
        }

# Election Class
class Election(Base):
    __tablename__ = 'election'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    party_id = Column(Integer, ForeignKey('party.id'))

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'year': self.year,
            'percentage': self.percentage
        }

# Popularity Class
class Popularity(Base):
    __tablename__ = 'popularity'

    id = Column(Integer, primary_key=True)
    state_name = Column(String(80), nullable=False)
    percentage = Column(Integer, nullable=False)
    party_id = Column(Integer, ForeignKey('party.id'))

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'state_name': self.state_name,
            'percentage': self.percentage
        }
# Growth class
class Growth(Base):
    __tablename__ = 'growth'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)

    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'year': self.year,
            'percentage': self.percentage
            }

engine = create_engine('sqlite:///polls.db')
Base.metadata.create_all(engine)
