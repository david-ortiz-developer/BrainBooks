from flask import Flask, render_template
from flask_babel import gettext as _
import json
import sqlite3
import uuid
import connection_manager as ConnMngr
import decimal

def board(token):
    print ("id ",str(uuid.uuid4()))
    menu_texts = { "one":_("Board"),
 "two": _("Tareas"),
 "three":  _("Marketplace"),
 "four": _("Minar"),
 "header-name": _("BB Board"),
 "actual-page": "board" }
    footer_translated_text = _("about-us") 

    user_info = ConnMngr.get_user_info(token)
    
    tasks_list = ConnMngr.getTasks(token)
    if len(tasks_list) < 1:
        tasks_list = "No Tasks"
    user_name = user_info['nombre']
    user_info['titulo_videos'] = _("Capacitación")
    calendar_list = ConnMngr.getEvents(user_info['uuid'])
    if len(calendar_list) < 1:
        calendar_list = "No events"
    wall_info = ConnMngr.getWall(token)

    learning_data = ConnMngr.getLearning()
    print("learning----------", learning_data)
    earnings_formatted = 13200
    user_info['earnings'] = earnings_formatted
    user_info['clusters'] = 3
    page = render_template("menu-logged.html",
menu_texts=menu_texts, token = token) + render_template("dashboard.html", user_info = user_info, calendar_list = calendar_list, tasks_list = tasks_list, wall_info = wall_info, learning_data = learning_data)+render_template("footer-not-logged.html", footer_text=footer_translated_text)
    return page