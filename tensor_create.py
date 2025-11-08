from flask import Flask, render_template
from flask_babel import gettext as _

def tensor_form(token):
    menu_texts = { "one":_("Board"),
 "two": _("Tareas"),
 "three":  _("MarketPlace"),
 "four": _("Mining"),
 "header-name": _("data Mining"),
 "actual-page": "mining" }
    footer_translated_text = _("about-us")
    page_texts = dict()
    page = render_template("menu-logged.html", menu_texts=menu_texts, token = token) + render_template("tensor_create.html")
    return page