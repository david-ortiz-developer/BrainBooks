from flask import Flask, render_template
from flask_babel import gettext as _

def loginForm(err_message):
    menu_texts = { "one":_("Home"),
 "two": _("Acceso"),
 "three":  _("Registro"),
 "four": _("Minar"),
 "header-name": _("BB Access"),
 "actual-page": "login" }
    footer_translated_text = _("about-us") 
    page_texts = {'email-placeholder':_("Correo Eléctronico")}
    page_texts['form-title'] = _("login")
    page_texts['pw-placeholder'] = _("Contraseña")
    page_texts['politics'] = _("La transparencia es lo mas importante para nosotros, por eso hemos diseñado nuestras politicas de forma amable y breve, por favor, tomate el tiempo de leerlas al menos una vez aquí ")
    page_texts['reset-pw'] = _("Resetear contraseña")
    page_texts['politics-link'] = _("políticas")
    page_texts['enter-button'] = _("Entrar")
    page = render_template("menu-not-logged.html",
menu_texts=menu_texts) + render_template("login.html", err_message = err_message, page_texts = page_texts)+render_template("footer-not-logged.html", footer_text=footer_translated_text)
    return page