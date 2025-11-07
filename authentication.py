from flask import Flask, render_template
import connection_manager as conn_mngr
from datetime import datetime

user = {"":""}

date_time = datetime(2016,10,1,0,0)
def login_user(user, password):
    result = conn_mngr.loginUser(user,password)
    try:
        if result['uuid']:
            user = result['uuid']
            date_time = datetime.today()
            print('start session ',date_time) 
            return result
    except:
        print("errore")
        date_time = datetime(2016,10,1,0,0)
        return {"error":"login"}
    return {"error":"login"}

def session_on():
    diference = datetime.today() - date_time
    print("session lleva ", diference, "session: ", session)  
    return true