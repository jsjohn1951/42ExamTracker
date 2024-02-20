from typing import List
from fastapi import FastAPI, HTTPException, WebSocket
from models import User, Status, NumBreaks, Server, ServStart, HistoryEntry, TMInfo
from wsManager import manager
from datetime import datetime, timedelta
from starlette.responses import FileResponse
# import pytz
from zoneinfo import ZoneInfo

app = FastAPI()
app.db = []
app.runtime = Server(examStart=ServStart.stopped)
app.breaks = NumBreaks(perFacility=3,perPerson=3)
app.History = []
app.timezone = None

def addHistory(user: User) :
	x = datetime.now(tz=ZoneInfo(app.timezone));
	time = x.strftime("%B %d, %Y %H:%M:%S");

	entry = HistoryEntry(id=user.id, user=user.user, event=user.status, time=time);
	app.History.append(entry);

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

@app.post("/api/timezone")
async def rtnTZInfo(timezone: TMInfo) :
	if (app.timezone == None) :
		app.timezone = timezone.tm;
	return (timezone);

@app.get("/api/breaks")
async def rtnBreaks() :
	return app.breaks

@app.post("/api/v1/start")
async def postStart(run: Server) :
	for item in app.db :
		item.status = Status.seated;
	app.runtime.examStart = run.examStart;

# posts
@app.post("/api/v1/users")
async def reg_user(user: User) :
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
	return user;

@app.post("/api/v1/breaks")
async def updateBreaks(recBreaks: NumBreaks) :
	app.breaks = recBreaks;
	for item in app.db :
		item.num = app.breaks.perPerson;
	return app.breaks;

def updateUser(item: User, update: User) :
	x = datetime.now(tz=ZoneInfo(app.timezone));
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

# Updates
@app.put("/api/v1/users")
async def up_user(update: User) :
	if (update.id != None and update.id != 0) :
		for item in app.db :
			if (item.id == update.id) :
				updateUser(item, update);
				addHistory(update);
				return ;
	elif (update.user != None and update.user != '') :
		for item in app.db :
			if (item.user == update.user) :
				updateUser(item, update);
				addHistory(update);
				return ;
	raise HTTPException(
		status_code = 404,
		detail=f"User '{update.user if update.user else update.id}' not found in Database!"
	)


# Web Sockets
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

# Deletes
@app.delete("/api/v1/users/clear")
async def clear() :
	app.db.clear();
	app.History.clear();
	return ("cleared database")

@app.delete("/api/v1/users/id/{id}")
async def rm_user(id: str) :
	usr_id = int(id);
	for item in app.db :
		if (item.id == usr_id) :
			return app.db.remove(item);
	raise HTTPException(
		status_code = 404,
		detail=f"User '{id}' not found in Database!"
	);

@app.delete("/api/v1/users/user/{id}")
async def rm_user(id: str) :
	for item in app.db :
		if (item.user == id) :
			return app.db.remove(item);
	raise HTTPException(
		status_code = 404,
		detail=f"User '{id}' not found in Database!"
	);