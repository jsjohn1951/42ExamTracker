from database import SessionLocal
from sqlalchemy.orm import Session
from schemas import User, NumBreaks, Status, Server, ServStart, HistoryEntry
from crud import get_users, get_breaks, get_isStarted, get_startTime, get_history
from datetime import datetime
from zoneinfo import ZoneInfo

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def setAppStarted() :
    started: ServStart = get_isStarted(SessionLocal());
    return (Server(examStart=started));

def setAppStartTm() :
    tm = get_startTime(SessionLocal());
    if (tm == None) :
        return (datetime.now(tz=ZoneInfo("Asia/Dubai")));
    print('------ Time Started: ', float(tm), ' -------');
    return (datetime.fromtimestamp(float(tm), tz=ZoneInfo("Asia/Dubai")));
        
def setAppUsers() :
    users = get_users(SessionLocal());
    appdb = [];
    print('---- init Users ----- : ', users);
    for item in users :
        appdb.append(User(id=item.id,
					user=item.user,
					gender=item.gender,
					status=item.status,
					num=item.num,
					time=item.time));
    print('------ users inserted! Returning ------');
    return (appdb);

def setAppHistory() :
    entries = get_history(SessionLocal());
    appEntr = [];
    print('---- init History ----- : ', entries);
    for item in entries :
        appEntr.append(HistoryEntry(id=item.id,
					user=item.user,
					event=item.event,
					time=item.time));
    print('------ users inserted! Returning ------');
    return (appEntr);

def setAppBreaks() :
    nbreaks = NumBreaks(perFacility=3,perPerson=3);
    breaks = get_breaks(SessionLocal());
    print('------ init breaks ------- : ', breaks);
    if (breaks != None) :
        nbreaks.perFacility = breaks.perfacility;
        nbreaks.perPerson = breaks.perperson;
    print('------ breaks inserted! Returning ------');
    return (nbreaks);

def updateUser(item: User, update: User, tz: ZoneInfo) :
	x = datetime.now(tz);
	time = x.strftime("%B %d, %Y %H:%M:%S");
	print('----- time: ', time, ' -----')
	stat: Status = item.status;
	if (item.status != update.status) :
		item.status = update.status;
	if (item.status == Status.away) :
		if (item.num > 0) :
			item.num = item.num - 1;
			item.time = time;
		else :
			item.status = stat;