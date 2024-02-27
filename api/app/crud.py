from sqlalchemy.orm import Session

from typing import List

from models import dbUser, dbBreaks, dbStarted, dbHistory, dbAdmin
from schemas import User, NumBreaks, ServStart, HistoryEntry, admin
from database import SessionLocal
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ! --------------------- Auth ---------------------

def create_admin(username: str, password: str) :
    db = SessionLocal();
    oldAdmin = db.query(dbAdmin).filter(dbAdmin.username == username).first();
    if (oldAdmin != None) :
        return None;
    dbusr: dbAdmin = dbAdmin(username=username,
                             hashauthentication=password);
    db.add(dbusr);
    db.commit();
    db.refresh(dbusr);
    return dbusr;

# ! --------------------- started ---------------------
def start(db: Session, tm: str) :
    db_start = db.query(dbStarted).first();
    if (db_start == None) :
        db_start = dbStarted(isstarted=True, timestarted=tm);
        db.add(db_start);
        db.commit();
        db.refresh(db_start);
    else :
        db_start.isstarted = True;
        db_start.timestarted = tm;
        db.commit();
    db_breaks = get_breaks(db);
    db_users = get_users(db);
    for item in db_users :
        item.num = db_breaks.perperson;
        db.commit();
    return db_start;

def shutdown(db: Session) :
    db_start = db.query(dbStarted).first();
    if (db_start == None) :
        db_start = dbStarted(isstarted=False, timestarted='');
        db.add(db_start);
        db.commit();
        db.refresh(db_start);
    else :
        db_start.isstarted = False;
        db_start.timestarted = '';
        db.commit();
    return db_start;

def get_isStarted(db: Session) :
    db_isStarted = db.query(dbStarted).first();
    if (db_isStarted != None and db_isStarted.isstarted) :
        return (ServStart.start);
    return (ServStart.stopped);

def get_startTime(db: Session) :
    db_isStarted = db.query(dbStarted).first();
    if (db_isStarted != None and db_isStarted.isstarted) :
        return (db_isStarted.timestarted);
    return (None);

# ! --------------------- Breaks ---------------------
def add_breaks(db: Session, breaks: NumBreaks) :
    db_breaks = dbBreaks(id=1,
                         perfacility=breaks.perFacility,
                         perperson=breaks.perPerson);
    db.add(db_breaks);
    db.commit();
    db.refresh(db_breaks);
    return db_breaks;

def get_breaks(db: Session) :
    return db.query(dbBreaks).filter(dbBreaks.id == 1).first();

def update_breaks(db: Session, breaks: NumBreaks) :
    db_breaks = get_breaks(db);
    db_breaks.perfacility = breaks.perFacility;
    db_breaks.perperson = breaks.perPerson;
    db.commit();
    return db_breaks;

# ! --------------------- Users ---------------------
def create_user(db: Session, user: User):
    db_user = dbUser(id=user.id,
                            user=user.user,
                            gender=user.gender,
                            status=user.status,
                            num=user.num,
                            time=user.time);
    db.add(db_user);
    db.commit();
    db.refresh(db_user);
    return db_user;

def get_user_id(db: Session, user_id: int):
    return db.query(dbUser).filter(dbUser.id == user_id).first();

def get_user_user(db: Session, username: str):
    return db.query(dbUser).filter(dbUser.user == username).first();

def get_users(db: Session):
    return db.query(dbUser).all();

def update_user(db: Session, user: User, id: bool = True):
    db_user: dbUser;
    if (id) :
        db_user = get_user_id(db, user.id);
    else :
        db_user = get_user_user(db, user.user);
    db_user.num = user.num;
    db_user.status = user.status;
    db_user.time = user.time;
    db.commit();
    return db_user;

def delete_user(db: Session, user: User, id: bool = True) :
    db_user: dbUser;
    if (id) :
        db_user = get_user_id(db, user.id);
    else :
        db_user = get_user_user(db, user.user);
    db.delete(db_user);
    db.commit();

# ! --------------------- History ---------------------
def add_History(db: Session, entry: HistoryEntry) :
    entry = dbHistory(id=entry.id,
                      user=entry.user,
                      event=entry.event,
                      time=entry.time);
    db.add(entry);
    db.commit();
    db.refresh(entry);
    return entry;

def get_history(db: Session) :
    return db.query(dbHistory).all();

def clear_history(db: Session) :
    history = get_history(db);
    for item in history :
        db.delete(item);
        db.commit();
    
