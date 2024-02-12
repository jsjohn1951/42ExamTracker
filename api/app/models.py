from pydantic import BaseModel
from typing import Optional
from enum import Enum

class Status(str, Enum) :
	seated = "SEATED"
	away = "AWAY"
	emergency = "EMERGENCY"

class Gender(str, Enum) :
	male = "Male"
	female = "Female"

class ServStart(str, Enum) :
	start = "STARTED"
	stopped = "NOT RUNNING"

class User(BaseModel) :
	id: Optional[int] = None
	user: Optional[str] = ''
	gender: Optional[Gender] = "Male"
	status: Optional[Status] = "SEATED"
	num: Optional[int] = 3

class NumBreaks(BaseModel) :
	perFacility: int
	perPerson: int

class Server(BaseModel) :
	examStart: Optional[ServStart] = "NOT RUNNING"