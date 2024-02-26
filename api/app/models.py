from pydantic import BaseModel
from typing import Optional
from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class dbUser(Base) :
	__tablename__ = "user"

	id = Column(Integer, unique=True, primary_key=True)
	user = Column(String, unique=True, index=True)
	gender = Column(String, index=True)
	status = Column(String, index=True)
	num = Column(Integer, index=True)
	time = Column(String, index=True)

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
	user = Column(String, index=True)
	event = Column(String, index=True)
	time = Column(String, index=True)