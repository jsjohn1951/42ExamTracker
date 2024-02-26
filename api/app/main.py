from typing import List
from fastapi import Depends, FastAPI, HTTPException, WebSocket
from schemas import User, Status, NumBreaks, Server, ServStart, HistoryEntry, TMInfo
from wsManager import manager
from datetime import datetime
from starlette.responses import FileResponse
from zoneinfo import ZoneInfo
from crud import start, shutdown, \
	get_isStarted, \
	add_breaks, get_breaks, \
	update_breaks, get_user_id, \
	get_user_user, get_users, \
	create_user, update_user, delete_user, \
	add_History, clear_history
from database import SessionLocal
from sqlalchemy.orm import Session
from utils import get_db, setAppUsers, \
	setAppStarted, setAppBreaks, updateUser, \
	setAppStartTm, setAppHistory
import os

app = FastAPI();
app.db = setAppUsers();
app.runtime = setAppStarted();
app.breaks = setAppBreaks();
app.History = setAppHistory();
app.timezone = None;
app.startTime = setAppStartTm();

def addHistory(user: User) :
	x = datetime.now(tz=ZoneInfo(app.timezone));
	time = x.strftime("%B %d, %Y %H:%M:%S");

	entry = HistoryEntry(id=user.id, user=user.user, event=user.status, time=time);
	app.History.append(entry);
	add_History(SessionLocal(), entry);

@app.get("/api")
def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_users() :
	return app.db;

@app.get("/api/v1/start")
async def isStart() :
	return app.runtime.examStart;

@app.get("/api/v1/users/away")
async def allAway() :
	listAll = [entry for entry in app.db if entry.status == Status.away];
	return listAll;

@app.get("/api/current/time")
async def rtnTime() :
	return str(datetime.now(tz=ZoneInfo(app.timezone)).timestamp())

@app.get("/api/history")
async def rtnHistory() :
	with open('Logfile.txt', mode='+w') as myfile :
		x = datetime.now(tz=ZoneInfo(app.timezone));
		time = x.strftime("%B %d, %Y");
		myfile.write('History Start:\t' + time + '\n\n');
		for item in app.History :
			line: str = '';
			if item.id != None :
				print('--- id: ', item.id, ' ----')
				line += str(item.id);
			else :
				line += item.user;
			line += '\t' + item.event + '\tTime: ' + str(item.time);
			myfile.write(line + '\n');
		myfile.close();
		return FileResponse('./Logfile.txt', media_type='application/octet-stream',filename='Logfile.txt')
	
@app.get("/api/history/{id}")
async def rtnIdHistory(id: str) :
	listAll = [entry for entry in app.History if entry.id == int(id)]
	with open('Logfile_'+id+'.txt', mode='+w') as myfile :
		x = datetime.now(tz=ZoneInfo(app.timezone));
		time = x.strftime("%B %d, %Y");
		myfile.write('History Start:\t' + time + '\n\n');
		for item in listAll :
			line: str = '';
			line += id;
			line += '\t' + item.event + '\tTime: ' + str(item.time);
			myfile.write(line + '\n');
		myfile.close();
		return FileResponse('Logfile_'+id+'.txt', media_type='application/octet-stream',filename='Logfile_'+id+'.txt')
	
@app.get("/api/time/startTime")
async def rtnStartTime() :
	return (app.startTime);

@app.post("/api/timezone")
async def rtnTZInfo(timezone: TMInfo) :
	if (app.timezone == None) :
		app.timezone = timezone.tm;
	return (timezone);

@app.get("/api/breaks")
async def rtnBreaks() :
	return app.breaks

# ! -------------------------------- posts  -------------------------------- 
@app.post("/api/v1/start")
async def postStart(run: Server, db: Session = Depends(get_db)) :
	for item in app.db :
		item.status = Status.seated;
	app.startTime = datetime.now(tz=ZoneInfo(app.timezone));
	app.runtime.examStart = run.examStart;
	if (app.runtime.examStart == ServStart.start) :
		start(db, str(app.startTime.timestamp()));
	else :
		shutdown(db);

@app.post("/api/v1/users")
async def reg_user(user: User, db: Session = Depends(get_db)) :
	if (user.id == 0 and user.user == '') :
		raise HTTPException(
			status_code = 400,
			detail=f"User can't have no id and no intra login!"
		);
	for item in app.db :
		if ((item.id != 0 and item.id == user.id) or \
		(item.user != '' and item.user == user.user)) :
			return user;
	user.num = app.breaks.perPerson;
	app.db.append(user);
	create_user(db=db, user=user);
	return user;

@app.post("/api/v1/breaks")
async def updateBreaks(recBreaks: NumBreaks, db: Session = Depends(get_db)) :
	app.breaks = recBreaks;
	for item in app.db :
		item.num = app.breaks.perPerson;
	if (get_breaks(db) == None) :
		add_breaks(db, app.breaks);
	else :
		update_breaks(db, app.breaks);
	return app.breaks;

# Updates
@app.put("/api/v1/users")
async def up_user(update: User, db: Session = Depends(get_db)) :
	if (update.id != None and update.id != 0) :
		for item in app.db :
			if (item.id == update.id) :
				updateUser(item, update, ZoneInfo(app.timezone));
				update_user(db, item);
				addHistory(update);
				return ;
	elif (update.user != None and update.user != '') :
		for item in app.db :
			if (item.user == update.user) :
				updateUser(item, update, ZoneInfo(app.timezone));
				update_user(db, item, False);
				addHistory(update);
				return ;
	raise HTTPException(
		status_code = 404,
		detail=f"User '{update.user if update.user else update.id}' not found in Database!"
	)


# ! -------------------------------- Web Sockets --------------------------------
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
	await manager.connect('all', websocket);
	try:
		while True:
			res = await websocket.receive_text();
			print('res: ', res);
			await manager.send_personal_message(res,websocket);
			await manager.broadcast(res, 'all', websocket);
	except Exception as e:
		print("Got an exception ",e);
		await manager.disconnect('all', websocket);

# ! -------------------------------- Deletes --------------------------------
@app.delete("/api/v1/users/clear")
async def clear(db: Session = Depends(get_db)) :
	for item in app.db :
		if (item.id != 0) :
			delete_user(db, item);
		else :
			delete_user(db, item, False);
	app.db.clear();
	clear_history(db);
	app.History.clear();
	dir = os.listdir('./')
	for item in dir :
		if item.endswith(".txt") :
			os.remove('./' + item);
	return ("cleared database")

@app.delete("/api/v1/users/id/{id}")
async def rm_user(id: str, db: Session = Depends(get_db)) :
	usr_id = int(id);
	for item in app.db :
		if (item.id == usr_id) :
			delete_user(db, item);
			return app.db.remove(item);
	raise HTTPException(
		status_code = 404,
		detail=f"User '{id}' not found in Database!"
	);

@app.delete("/api/v1/users/user/{id}")
async def rm_user(id: str, db: Session = Depends(get_db)) :
	for item in app.db :
		if (item.user == id) :
			delete_user(db, item, False);
			return app.db.remove(item);
	raise HTTPException(
		status_code = 404,
		detail=f"User '{id}' not found in Database!"
	);