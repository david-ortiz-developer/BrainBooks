from flask import Flask, render_template
from flask_babel import gettext as _
import connection_manager as ConnMngr
import uuid




def show_model(model_id):
    model_selected = ConnMngr.open_model(model_id)
    print(model_selected)
    token = "1"
    menu_texts = { "one":_("Board"),
 "two": _("Tareas"),
 "three":  _("MarketPlace"),
 "four": _("Mining"),
 "header-name": _("data Mining"),
 "actual-page": "mining" }
    footer_translated_text = _("about-us")
    page_texts = dict()
    page_texts["title"] = _(model_selected[0]['name'])
    page_texts["header"] = _("Dataset Builder")
    page_texts['add-row'] = _("Añadir variable (Vector)")
    page_texts['clean-row'] = _("Limpiar todo")
    page_texts["description"] = _(model_selected[0]['description'])
    page_texts['rows-name'] = _("variables")
    page_texts["subtitle"] = _("Tus modelos son gemas")
    page_texts['red-warning'] = _("No se te olvide guardar la nueva data oprimiendo el botón de abajo SUBIR FILAS, para no perder tu trabajo")
    page_texts['disclamier'] = _("Al servidor se suben las filas y las imágenes clasificadas temporalmente.")
    page_texts['explanation1'] = _("Formato CSV:")
    page_texts['explanation2'] = _(" id, titulo, descripcion, categoria, imagenes (pipe-separated)")
    page_texts['explanation3'] = _("Ejemplo:")
    page_texts['explanation4'] = _("uuid-1, Gato, foto de gato, animales, gato1.jpg|gato2.jpg")
    page_texts['dataset-name'] = _("Nombre del dataset")
    page_texts['upload-row'] = _("SUBIR FILA")
    page_texts['compile-button'] = _("COMPILAR Y ENTRENAR MODELO")
    page_texts['note1'] = _("Nota:")
    page_texts['note2'] = _(" Los archivos de imagen se eliminan tan pronto el modelo termina su entrenamiento. No suba ningúna imagen al servidor que comprometa su privacidad.")
    page_texts['subir'] = _("Subir")
    page_texts['limpiar'] = _("Limpiar")
    page_texts['duplicar'] = _("Duplicar")
    page_texts['delete'] = _("Eliminar")
    page_texts['row-id'] = uuid.uuid5(uuid.NAMESPACE_DNS, 'brainsbook')
    page_texts["volver"] = _("Volver")

    rows_count = ConnMngr.get_rows(model_id)
    print(f"rows {rows_count}")
    page_texts['count'] = rows_count
    page = render_template("menu-logged.html", menu_texts=menu_texts, token = token)+ render_template("model_details.html", page_texts = page_texts, model_id = model_id) +render_template("footer-not-logged.html", footer_text=footer_translated_text)
    if token == "show":
        return render_template("model_details.html", page_texts = page_texts)
    return page