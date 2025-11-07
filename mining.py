from flask import Flask, render_template
from flask_babel import gettext as _

def mining_page(token):
    menu_texts = { "one":_("Board"),
 "two": _("Tareas"),
 "three":  _("Pagos"),
 "four": _("Mining"),
 "header-name": _("data Mining"),
 "actual-page": "mining" }
    footer_translated_text = _("about-us")
    page = render_template("menu-logged.html", menu_texts=menu_texts, token = token) + render_template("mining.html")+render_template("footer-not-logged.html", footer_text=footer_translated_text)
    if token == "show":
        return render_template("show-example.html")
    return page