from flask import Flask, render_template
from flask_babel import gettext as _

def app_onboard(page_route: str, header_name: str):
    """In order to acomplish localization all texts are rendered here and passed to the template. page_route: defines the actual page. header_name: is the html meta tag for the header of the page.""" 
#Header menu
    menu_texts = { "one":_("Home"),
 "two": _("Acceso"),
 "three":  _("Registro"),
 "four": _("Minar"),
 "header-name": header_name,
 "actual-page": page_route }
#Body
    bodyTexts = {"image1Name": _("static/img/home-poducs-1.PNG"),
"itemName1": _("Recolección y curaduría de Big Datasets"), "itemText1": _("Licencias de acceso, dataset-as-a-service para visión articicial, mapas semanticos para navegación indoor, datos de precisión de movimiento y reconocimiento de gestos humanos."), "itemName2": _("Modelos de Aprendizaje Automático Pre-Entrenados"), "itemText2": _("APIs de suscripción a modelos Predictive Maintenance para detección de anomalias. Modelos de lenguaje natural simplificado adaptable para la crisis, Crisis Awareness"),
"itemName3": _("API de Modelos con Integración Colaborativa"),
"itemText3": _("Permitir que varias empresas datificadas entrenen modelos de forma colaborativa sin compartir datos sensibles (cada fábrica entrena en local y comparte solo los gradientes)."),
"itemName4": _("Gemelos Digitales Basados en Datos"),
"itemText4": _("licencias 👉Digital Twin, servicios de simulación e integracion de modelos que se alimentan en tiempo real con datos no sensibles. Esto permite predecir respuestas en simuladores antes de interactuar en entornos reales."), 
"itemName5": _("Optimización / Reciclaje para Bases de Datos"),
"itemText5": _("Convierte cada byte en capital líquido, la economía guiada por datos nunca duerme. Data-as-a-Product (DaaP), tratamos los datos como un activo empaquetado, versionado y comercializable."), 
"itemName6": _("Consultoría + desarrollo a medida"),
"itemText6": _("Empujamos tu organizacion a pensar, sentir y decidir en lenguaje de datos. Cultura empresarial donde los participantes son conscientes de como cambios milimétricos pueden desencadenar transformaciones globales."), 
"itemName7": _("Marketplace de modelos"),
"itemText7": _("La Nueva Minería Invisible, monetización múltiple de la información, si el siglo XX se definió por las fábricas y el petróleo, el siglo XXI lo definirá quien sepa transformar datos en sabiduría."), 
"itemName8": _("Blockchain Secure Access + Data tokens con trazabilidad"),
"itemText8": _("Preciosos Datos como NFT, Cuándo y cómo fue capturado el dato. Si ha sido alterado. Cuántas veces ha cambiado de propietario"), "image2Name": _("static/img/home-poducs-2.PNG"), "image3Name": _("static/img/home-poducs-3.PNG"),"image4Name": _("static/img/home-poducs-4.PNG"),"image5Name": _("static/img/home-poducs-5.PNG"), "image6Name": _("static/img/home-poducs-6.PNG"), "image7Name": _("static/img/home-poducs-7.PNG"), "image8Name": _("static/img/home-poducs-8.PNG"), "paragraph1": _("paragraph1")}
#Footer
    footer_translated_text = _("about-us") 
#Render
    page = render_template("menu-not-logged.html",
menu_texts=menu_texts) + render_template("body-not-logged.html",
bodyTexts=bodyTexts) + render_template("footer-not-logged.html", footer_text=footer_translated_text)
    return page