from flask import Flask, render_template
from flask_babel import gettext as _
import connection_manager as ConnMngr

def show_data(model_id, model_name):
    menu_texts = { "one":_("Board"),
 "two": _("Tareas"),
 "three":  _("MarketPlace"),
 "four": _("Mining"),
 "header-name": _("data Mining"),
 "actual-page": "mining" }
    footer_translated_text = _("about-us")
    page_texts = dict()
    page_texts["title"] = _("Data Gold Mine")
    page_texts["volver"] = _("Volver")
    page_texts['edit-cell'] = _("Editar")
    page = 1
    page_texts['model-name'] = model_name
    first_twelve = ConnMngr.getData(model_id, (page * 12))

    page = render_template("menu-logged.html", menu_texts=menu_texts, token = model_id) + render_template("model_data.html", page_texts = page_texts, first_twelve = first_twelve)+render_template("footer-not-logged.html", footer_text=footer_translated_text)
    if model_id == "show":
        return render_template("show-example.html")
    return page