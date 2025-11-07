from flask import Flask, render_template
from flask_babel import gettext as _
import connection_manager as ConnMngr

def models_board(token):
    models_list = ConnMngr.get_models()
    menu_texts = { "one":_("Board"),
 "two": _("Tareas"),
 "three":  _("MarketPlace"),
 "four": _("Mining"),
 "header-name": _("data Mining"),
 "actual-page": "mining" }
    footer_translated_text = _("about-us")
    page_texts = dict()
    page_texts["title"] = _("Data Gold Mine")
    page_texts["subtitle"] = _("Tus modelos son gemas")
    page_texts["progress-text"] = _("progreso")
    page_texts['tensors-text'] = _("tensores")
    page_texts['new-model'] = _("NUEVO MODELO")
    page_texts['description-placeholder'] = _("Descripción del modelo")
    page_texts['new-name-placeholder'] = _("Nombre del modelo")
    page_texts['create'] = _("Crear")

    page = render_template("menu-logged.html", menu_texts=menu_texts, token = token) + render_template("models.html", page_texts = page_texts, models = models_list)+render_template("footer-not-logged.html", footer_text=footer_translated_text)
    if token == "show":
        return render_template("show-example.html")
    return page