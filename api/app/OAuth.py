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
secret_key = os.getenv('SECRET');
ALGO = "HS256";
ACCESS_TOKEN_EXPIRE_MINUTES = 5;

def create_token(data: dict) :
    to_encode = data.copy();
    ex = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES);
    to_encode.update({"expire" : ex.strftime("%Y-%m-%d %H:%M:%S")});
    encoded_jwt = jwt.encode(to_encode, secret_key, ALGO);
    return encoded_jwt;

def verify_token(token: str, credentials_exception) :
    try:
        payload = jwt.decode(token, secret_key, ALGO);
        id: str = payload.get("user_id");
        print('TIME NOW:      ', datetime.utcnow())
        print('TOKEN EXPIRES: ', payload.get("expire"))
        if (id == None) :
            raise credentials_exception;
        token_data = schemas.DataToken(id=id);
    except JWTError as e:
        print (e);
        raise credentials_exception;
    return token_data;

def get_current_user(token : str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credential_execption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Unrecognized User",
                                         headers={"www-Authenticate" : "Bearer"});
    print('------  was checked!  --------')
    token = verify_token(token, credential_execption);
    user = db.query(models.dbAdmin).filter(models.dbAdmin.username == token.id).first();
    return user;