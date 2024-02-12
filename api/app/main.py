from typing import List
from fastapi import FastAPI, HTTPException, WebSocket
from models import User, Status, NumBreaks, Server, ServStart
from wsManager import manager

app = FastAPI()

app.db = []

app.runtime = Server(examStart=ServStart.stopped)

app.breaks = NumBreaks(perFacility=3,perPerson=3)

async def updater(item : User, update : User) :
	if item.status != update.status : 
		if update.status == Status.away :
			if item.num == 0 :
				raise HTTPException(
					status_code = 404,
					detail=f"User '{update.user}' has no more breaks!"
				);
			item.num -= 1;
		item.status = update.status;
	if item.gender != update.gender : item.gender == update.gender;
	return item

@app.get("/api")
def read_root():
    return {"Hello": "World"}

@app.get("/api/v1/users")
async def fetch_users() :
	return app.db;


@app.get("/api/v1/start")
async def isStart() :
	return app.runtime.examStart;

@app.post("/api/v1/start")
async def postStart(run: Server) :
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
	app.db.append(user);
	return user;

@app.post("/api/v1/breaks")
async def updateBreaks(recBreaks: NumBreaks) :
	app.breaks = recBreaks;
	for item in app.db :
		item.num = app.breaks.perPerson;
	return app.breaks;



# Updates
@app.put("/api/v1/users")
async def up_user(update: User) :
	for item in app.db :
		if (item.id == update.id or item.user == update.user) :
			item = await updater(item, update)
			return
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
			await websocket.receive_text();
			await manager.send_personal_message("Updating all",websocket);
			await manager.broadcast('Update All', 'all', websocket);
	except Exception as e:
		print("Got an exception ",e);
		await manager.disconnect('all', websocket);



# Deletes
@app.delete("/api/v1/users/clear")
async def clear() :
	app.db.clear();
	return ("cleared database")

@app.delete("/api/v1/users/{name}")
async def rm_user(name: str) :
	for item in app.db :
		if (item.f_name == name) :
			return app.db.remove(item)
	raise HTTPException(
		status_code = 404,
		detail=f"User '{name}' not found in Database!"
	)