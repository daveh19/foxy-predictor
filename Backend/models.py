from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Enum, create_engine, Float, func, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATE, TIME, DATETIME
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()


class Party(Base):
    __tablename__ = 'party'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    abbreviation = Column(String(80), nullable=False)
    leader = Column(String(80), nullable=False)
    alliance = Column(String(80), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'abbreviation': self.abbreviation,
            'leader': self.leader,
            'alliance': self.alliance
        }


class Election(Base):
    __tablename__ = 'election'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    party = relationship(Party)
    party_id = Column(Integer, ForeignKey('party.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'year': self.year,
            'percentage': self.percentage,
            'party_id': self.party_id
        }

class Growth(Base):
    __tablename__ = 'growth'

    id = Column(Integer, primary_key=True)
    year = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'year': self.year,
            'percentage': self.percentage
            }





engine = create_engine('sqlite:///polls.db')
Base.metadata.create_all(engine)
