from flask import Flask, render_template, jsonify
from flask_babel import gettext as _
import json
import sqlite3
from datetime import datetime
import uuid
import urllib.parse

DB_FILE = "bb_comunity.db"

def setupDatabase():
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS models (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        columns INTEGER NOT NULL,
        progress INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS rows (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_id INTEGER NOT NULL,
        row_index INTEGER NOT NULL,
        FOREIGN KEY(model_id) REFERENCES models(id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS cells (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        row_id INTEGER NOT NULL,
        column_index INTEGER NOT NULL,
        text_value TEXT,
        FOREIGN KEY(row_id) REFERENCES rows(id)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS images (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cell_id INTEGER NOT NULL,
        image_path TEXT NOT NULL,
        FOREIGN KEY(cell_id) REFERENCES cells(id)
    )""")

def getWall(user_id):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    return_list = []
    for row in cur.execute('SELECT id, author, text, time, rating, action, people, author_id FROM  "activity" WHERE ("people" LIKE "all") LIMIT 12 OFFSET 0;'):
        date_str = row[3]
        today = datetime.today()
        date_event = datetime.strptime(date_str, "%d/%m/%y %H:%M")
        interval = today - date_event
        time_text = ""
        if interval.days > 0:
            time_text = str(interval.days) + "d"
        elif interval.seconds > 0:
            if interval.seconds < 3600:
                time_text = str(int(interval.seconds/60)) + "m"
            else:
                time_text = str(int((interval.seconds/60)/60)) + "h"          
        print("interval ", time_text)
        return_list.append({"author": row[1], "text": row[2], "time": time_text, "rating": row[4], "action": row[5], "author_id": row[7]})
    print("wall +++++++++++++", return_list)
    return return_list

def getTasks(user_id):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    return_list = []
    for row in cur.execute('SELECT id, name, description, progress, dependencies, people, owner, eta FROM  "tasks" WHERE ("people" LIKE "%'+user_id+'%") LIMIT 12 OFFSET 0;'):
        return_list.append({"title": row[1], "progress": row[3], "eta": 3})
    
    return return_list

def getLearning(user_id = 1):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    return_list = []
    for row in cur.execute('SELECT uuid, name, path, duration FROM  "learning" WHERE ("level" == "'+str(user_id)+'") LIMIT 12 OFFSET 0;'):
        return_list.append({"uuid": row[0], "name": row[1], "path": row[2], "duration": row[3]})
    return return_list

def getEvents(user_id):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    return_list = []
    for row in cur.execute('SELECT id, day, people, note FROM  "events" WHERE ("people" LIKE "%'+user_id+'%") LIMIT 12 OFFSET 0;'):
        note_str = row[3]
        date_str = row[1]
        date_event = datetime.strptime(date_str, "%d/%m/%y %H:%M")
        return_list.append({"day":date_event.strftime('%d'), "date": date_event.strftime('%a'), "note": note_str})
    return return_list
      
def get_user_info(token):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    print(token)
    query_str = 'SELECT id, email, pw, nombre, nivel, puntos, descripcion, progress, tasks_done, tasks_total, uuid, nickname FROM "users" WHERE ("uuid" == "'+token+'")'
    for row in cur.execute(query_str):
        payload = {"uid": row[0], "user":row[2], "nombre": row[3], "nivel": row[4], "puntos": row[5], "descripcion": row[6], "progress": row[7], "tasks_done": row[8], "tasks_total": row[9], "uuid": row[10], "nickname": row[11]}
        print("user info", row)
        return payload
    return {"error":"can not login"}

def loginUser(user, pw):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    query_str = 'SELECT pw, uuid FROM "users" WHERE ("email" == "'+user.lower()+'")'
    for row in cur.execute(query_str):
        if pw == row[0]:
            payload = {"uuid": row[1]}
            print('logged', row)
            return payload
    return {"error":"can not login"}

def create_model(name, columns, description):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    date_str = str(datetime.today())
    safe_name = urllib.parse.quote(name)
    safe_description = urllib.parse.quote(description)
    print("safe", safe_name, safe_description) 
    now = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f") 
    query_str = 'INSERT INTO "models" ("name", "columns", "progress", "created_at", "description") VALUES ("'+safe_name+'", "'+str(columns)+'", "0", "'+str(now)+'", "'+safe_description+'")'
    response = cur.execute(query_str)
    print("response", response)
    conn.commit()
    conn.close()

def get_models():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    user_level = 1
    return_list = []
    for row in cur.execute('SELECT id, name, columns, progress, created_at, level FROM  "models" WHERE ("level" <= '+str(user_level)+') ORDER BY created_at DESC LIMIT 12 OFFSET 0;'):
        safe_name = urllib.parse.unquote(row[1])
        return_list.append({"id": row[0], "name": safe_name, "columns": row[2], "progress": row[3], "created_at": row[4]})
    return return_list

def open_model(model_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return_list = []
    for row in cur.execute("SELECT * FROM models WHERE id=?", (model_id,)):
        safe_name = urllib.parse.unquote(row[1])
        safe_description = ""
        try:
            safe_description = urllib.parse.unquote(row[6])
        except:
            safe_description = "" 
        return_list.append({"id": row[0], "name": safe_name, "columns": row[2], "progress": row[3], "created_at": row[4], "description": safe_description})
    conn.close()
    return return_list 
 
def create_rows(datos, model_id):
    """ sql wrapper for inserting new cells """
    new_cell_id = uuid.uuid1()
    sql_row_string = 'INSERT INTO "rows" ("id", "model_id", "parent_row") VALUES '
    sql_row_string += f"(NULL, {model_id}, '{new_cell_id}');"
    sql_cell_string = 'INSERT INTO "cells" ("id", "row_id", "column_index", "text_value", "tensor_value", "tensor_category") VALUES '
    index = -1
    for data_vector in datos:
        index += 1
        sql_cell_string += f'(NULL, "{new_cell_id}", "{data_vector["id"]}", "{data_vector["titulo"]}", "{data_vector["descripcion"]}",  "{data_vector["categoria"]}")'
        if index == (len(datos) - 1):
            sql_cell_string += ";"
        else:
            sql_cell_string += ","
    print(f"ready to save {()}")
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor() 
    print(f"executing {sql_row_string}") 
    response = cur.execute(sql_row_string)
    print("response", response)
    conn.commit()
    print(f"executing {sql_cell_string}") 
    response2 = cur.execute(sql_cell_string)
    conn.commit()
    conn.close()
    return ({"result":True})

def get_rows(model_id):
    count_sql_string = f'SELECT COUNT(*) FROM "rows" WHERE model_id == {model_id}'
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    print(f"executing {count_sql_string}")
    res = cur.execute(count_sql_string)
    count = res.fetchone()
    print(f"rooowww {count[0]}")
    return count[0]

def getData(model_id, offset):
    rows_sql_string = f'SELECT * FROM "rows" WHERE model_id == {model_id}'
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur2 = conn.cursor()
    print(f"executing {rows_sql_string}")
    return_list = []
    for row in cur.execute(rows_sql_string):
        cells_sql_string = f'SELECT * FROM "cells" WHERE row_id == "{row[2]}"'
        print(f"executing {cells_sql_string}")
        cells = []
        for cell in cur2.execute(cells_sql_string):
            cells.append(cell)
            print(f"getting {cell[3]} = {cell[4]}")
        return_list.append({"row": row, "cells": cells})
    return return_list
    
    
    
