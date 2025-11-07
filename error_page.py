from flask import Flask, render_template
from flask_babel import gettext as _


    


def showError():
    menu_texts = { "one":_("Home"),
 "two": _("Acceso"),
 "three":  _("Registro"),
 "four": _("Minar"),
 "header-name": _("BB Access"),
 "actual-page": "login" }
    footer_translated_text = _("about-us") 
    page = render_template("menu-not-logged.html",
menu_texts=menu_texts) + render_template("not_found.html")+render_template("footer-not-logged.html", footer_text=footer_translated_text)
    return page