from datetime import timedelta, datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from database import SessionLocal
import schemas
import models
import os

def get_db():
    db = SessionLocal();
    try:
        yield db;
    finally:
        db.close();
        
oauth2_schema = OAuth2PasswordBearer(tokenUrl='api/login');
SECRET = os.getenv('SECRET');
ALGO = os.getenv('ENCRYPTION_ALGO');
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'));

def create_token(data: dict) :
    to_encode = data.copy();
    ex = datetime.utcnow() + timedelta(days=0, minutes=ACCESS_TOKEN_EXPIRE_MINUTES);
    to_encode.update({"expire" : ex.strftime("%Y-%m-%d %H:%M:%S")});
    encoded_jwt = jwt.encode(to_encode, SECRET, ALGO);
    return encoded_jwt;

def verify_token(token: str, unknown_user, expired) :
    try:
        payload = jwt.decode(token, SECRET, ALGO);
        id: str = payload.get("user_id");
        time_remaining = datetime.strptime(payload.get("expire"), "%Y-%m-%d %H:%M:%S") - datetime.utcnow()
        print('EXPIRES:       ', time_remaining)
        if (time_remaining.total_seconds() < 0) :
            raise expired;
        if (id == None) :
            raise unknown_user;
        token_data = schemas.DataToken(id=id);
    except JWTError as e:
        print (e);
        raise unknown_user;
    return token_data;

def get_current_user(token : str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credential_execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Unrecognized User",
                                         headers={"www-Authenticate" : "Bearer"});
    expired = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Expired Token",
                                         headers={"www-Authenticate" : "Bearer"});
    print('------  was checked!  --------')
    token = verify_token(token, credential_execption, expired);
    user = db.query(models.dbAdmin).filter(models.dbAdmin.username == token.id).first();
    return user;