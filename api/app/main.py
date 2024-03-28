from typing import List
from fastapi import Depends, APIRouter, FastAPI, HTTPException, WebSocket, status
from fastapi.security import OAuth2PasswordRequestForm
from schemas import User, Status, NumBreaks, Server, ServStart, HistoryEntry, TMInfo, admin, Token
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
	add_History, clear_history, create_admin, get_admin
from database import SessionLocal
from sqlalchemy.orm import Session
from utils import get_db, setAppUsers, \
	setAppStarted, setAppBreaks, updateUser, \
	setAppStartTm, setAppHistory, hash_pass, verify_password
from OAuth import create_token, get_current_user, oauth2_schema
import os
from typing_extensions import Annotated

app = FastAPI();
app.db = setAppUsers();
app.runtime = setAppStarted();
app.breaks = setAppBreaks();
app.History = setAppHistory();
app.timezone = None;
app.startTime = setAppStartTm();

create_admin(username=os.getenv("ADMIN_USR"), password=hash_pass(os.getenv("ADMIN_PW")));

def addHistory(user: User) :
	x = datetime.now(tz=ZoneInfo(app.timezone));
	time = x.strftime("%B %d, %Y %H:%M:%S");

	entry = HistoryEntry(id=user.id, user=user.user, event=user.status, time=time);
	app.History.append(entry);
	add_History(SessionLocal(), entry);

@app.post("/api/validate",  tags=['Authenticate'])
def validation(token: Token, db: Session = Depends(get_db)):
	get_current_user(token.access_token, db);
	return (True);

@app.post("/api/login", response_model=Token, tags=['Authenticate'])
def login(userdetails: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) :
	user = get_admin();
	if not user or user.username != userdetails.username :
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User Not Found");
	if not verify_password(userdetails.password, user.hashauthentication) :
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Password Mismatch");
	access_token = create_token({"user_id" : user.username});
	return {"access_token" : access_token, "token_type" : "bearer"};

@app.get("/api/v1/users", tags=['Entries'])
async def fetch_users(token: Annotated[str, Depends(get_current_user)]) :
	return app.db;

@app.get("/api/v1/start", tags=['Runtime'])
async def isStart(token: Annotated[str, Depends(get_current_user)]) :
	return app.runtime.examStart;

@app.get("/api/v1/users/away", tags=['Status Away'])
async def allAway(token: Annotated[str, Depends(get_current_user)]) :
	listAll = [entry for entry in app.db if entry.status == Status.away];
	return listAll;

@app.get("/api/current/time", tags=['Time'])
async def rtnTime(token: Annotated[str, Depends(get_current_user)]) :
	return str(datetime.now(tz=ZoneInfo(app.timezone)).timestamp())

@app.get("/api/history", tags=['History'])
async def rtnHistory(token: Annotated[str, Depends(get_current_user)]) :
	with open('Logfile.txt', mode='+w') as myfile :
		x = datetime.now(tz=ZoneInfo(app.timezone));
		time = x.strftime("%B %d, %Y");
		myfile.write('History Start:\t' + time + '\n\n');
		for item in app.History :
			line: str = '';
			if item.id != None and item.id != 0 :
				print('--- id: ', item.id, ' ----')
				line += str(item.id);
			else :
				line += item.user;
			line += '\t' + item.event + '\tTime: ' + str(item.time);
			myfile.write(line + '\n');
		myfile.close();
		return FileResponse('./Logfile.txt', media_type='application/octet-stream',filename='Logfile.txt')

@app.get("/api/history/{id}", tags=['History'])
async def rtnIdHistory(token: Annotated[str, Depends(get_current_user)], id: str) :
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

@app.get("/api/time/startTime", tags=['Time'])
async def rtnStartTime(token: Annotated[str, Depends(get_current_user)]) :
	return (app.startTime);

@app.post("/api/timezone", tags=['Time'])
async def rtnTZInfo(token: Annotated[str, Depends(get_current_user)], timezone: TMInfo) :
	if (app.timezone == None) :
		app.timezone = timezone.tm;
	return (timezone);

@app.get("/api/breaks", tags=['Breaks'])
async def rtnBreaks(token: Annotated[str, Depends(get_current_user)]) :
	return app.breaks

# ! -------------------------------- posts  --------------------------------
@app.post("/api/v1/start", tags=['Runtime'])
async def postStart(token: Annotated[str, Depends(get_current_user)], run: Server, db: Session = Depends(get_db)) :
	for item in app.db :
		item.status = Status.seated;
	app.startTime = datetime.now(tz=ZoneInfo(app.timezone));
	app.runtime.examStart = run.examStart;
	if (app.runtime.examStart == ServStart.start) :
		start(db, str(app.startTime.timestamp()));
	else :
		shutdown(db);

@app.post("/api/v1/users", tags=['Entries'])
async def reg_user(token: Annotated[str, Depends(get_current_user)], user: User, db: Session = Depends(get_db)) :
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

@app.post("/api/v1/breaks", tags=['Breaks'])
async def updateBreaks(token: Annotated[str, Depends(get_current_user)], recBreaks: NumBreaks, db: Session = Depends(get_db)) :
	app.breaks = recBreaks;
	for item in app.db :
		item.num = app.breaks.perPerson;
	if (get_breaks(db) == None) :
		add_breaks(db, app.breaks);
	else :
		update_breaks(db, app.breaks);
	return app.breaks;

# Updates
@app.put("/api/v1/users", tags=['Entries'])
async def up_user(token: Annotated[str, Depends(get_current_user)], update: User, db: Session = Depends(get_db)) :
	if (update.id != None and update.id != 0) :
		print ("<DAMMIT HERE!>>>>>>>>>> Update id: ", update.id)
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
@app.delete("/api/v1/users/clear", tags=['Delete'])
async def clear(token: Annotated[str, Depends(get_current_user)], db: Session = Depends(get_db)) :
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

@app.delete("/api/v1/users/id/{id}", tags=['Delete'])
async def rm_user(token: Annotated[str, Depends(get_current_user)], id: str, db: Session = Depends(get_db)) :
	usr_id = int(id);
	for item in app.db :
		if (item.id == usr_id) :
			delete_user(db, item);
			return app.db.remove(item);
	raise HTTPException(
		status_code = 404,
		detail=f"User '{id}' not found in Database!"
	);

@app.delete("/api/v1/users/user/{id}", tags=['Delete'])
async def rm_user(token: Annotated[str, Depends(get_current_user)], id: str, db: Session = Depends(get_db)) :
	for item in app.db :
		if (item.user == id) :
			delete_user(db, item, False);
			return app.db.remove(item);
	raise HTTPException(
		status_code = 404,
		detail=f"User '{id}' not found in Database!"
	);