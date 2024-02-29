from pydantic import BaseModel
from typing import Optional
from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class dbUser(Base) :
	__tablename__ = "dbuser"

	id = Column(Integer, unique=True, primary_key=True)
	user_id = Column(String, unique=True, index=True)
	gender = Column(String, index=True)
	usr_status = Column(String, index=True)
	num = Column(Integer, index=True)
	time_stamp = Column(String, index=True)

class dbBreaks(Base) :
	__tablename__ = "breaks"

	id = Column(Integer, unique=True, primary_key=True)
	perfacility = Column(Integer, index=True)
	perperson = Column(Integer, index=True)

class dbStarted(Base) :
	__tablename__ = "started"

	isstarted = Column(Boolean, primary_key=True)
	timestarted = Column(String, index=True);

class dbHistory(Base) :
	__tablename__ = "history"

	id = Column(Integer, primary_key=True)
	user_id = Column(String, index=True)
	event_oc = Column(String, index=True)
	time_stamp = Column(String, index=True)

class dbAdmin(Base) :
	__tablename__ = "admin"

	username = Column(String, primary_key=True)
	hashauthentication = Column(String, index=True)