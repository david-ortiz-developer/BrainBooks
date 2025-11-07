from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_babel import gettext as _
import login
import home_not_logged
import dashboard
#import models_showroom as modelos
#import register
import mining as mineria
import models
import error_page as err
import authentication as auth
from flask_babel import Babel
import os
import csv
import connection_manager as conn_mngr
import models_detail
import JWTAuthenticator as jwtauth
import model_data

def create_app():
## returns the app with babel and flask on it.
    def get_locale():
        lang = request.args.get('lang')
        if lang:
            return lang
        return 'es'

    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='dev',
        BABEL_DEFAULT_LOCALE='es',
        BABEL_DEFAULT_TIMEZONE='UTC',
        LANGUAGES={'en': 'English', 'es': 'Español'},
    )
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'locales'
    babel.init_app(app, locale_selector=get_locale)
    return app

babel = Babel()
app = create_app()

app.config['JWT_SECRET_KEY'] = ':)god_is_good!'
app.config['JWT_ALGORITHM'] = 'HS256'
app.config['JWT_EXPIRATION_TIME'] = 3600

jwt_manager = jwtauth.JWTAuthenticator(app)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)  
login_payload = {"error":"login"} 
  

@app.route('/')
def welcome_friend():
    token = request.args.get("token")
    if token == None:
        return app_onboard()
    return app_dashboard('0dcec603-054c-427b-bb38-85b765fbc0cc')  
 
@app.route("/login", methods=["GET"]) 
def login_form():
    return login.loginForm("")

@app.route("/board", methods=["GET"])
def my_board():    
    return app_dashboard(login_payload) 

@app.route("/login", methods=["POST"])
def login_auth():
    userName = request.form["email"]
    error_code = login.loginForm(err_message=_("Error iniciando sesión, revisa el email y la contraseña e intenta de nuevo"))
    login_payload = auth.login_user(userName, request.form["pw"])
    if login_payload == {"error":"login"}:
        print("error payload")
        return error_code
    elif login_payload['uuid']:
        return app_dashboard(login_payload['uuid'])
    return error_code

@app.route("/mining", methods=["GET"])
def mining():
    token = request.args.get("token")
    if token:
        return mining_page(token)
    return login.loginForm(_("tienes que iniciar sesión"))

@app.route("/mining_board")
def mining_board():
    token = request.args.get("token")
    if token:
        return models.models_board(token)
    return login.loginForm(_("tienes que iniciar sesión"))

@app.route("/create_model", methods=["POST"])
def create_model():
    name = request.form.get("name")
    columns = request.form.get("columns", type=int)
    description = request.form.get("description")
    image = request.files.get("image")
    image_path = None
    if image and image.filename:
        filename = f"{name}_{image.filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image.save(filepath)
        image_path = filepath
    conn_mngr.create_model(name, columns, description)
    return redirect(url_for("mining_board")+"?token=3426342653465")
       
@app.route("/model/<int:model_id>")
def model_detail(model_id):
    return models_detail.show_model(model_id)

@app.route("/procesar/<int:model_id>", methods=["POST"])
def procesar(model_id):
    datos = request.get_json()
    result = conn_mngr.create_rows(datos, model_id)
    return jsonify({"result": result})

@app.route("/data/<int:model_id>", methods=["GET"])
def ver(model_id):
    model_name = request.args.get('model_name')
    return model_data.show_data(model_id, model_name=model_name)

@app.route('/generate-token', methods=['POST'])
def generate_token():
    payload = {'user_id': 1, 'username': 'testuser'}
    token = jwt_manager.encode_token(payload)
    return {'token': token}

@app.route('/verify-token', methods=['POST'])
def verify_token():
    token = request.json.get('token')
    if not token:
        return {'error': 'Token is missing'}, 400
    decoded_payload = jwt_manager.decode_token(token)
    if isinstance(decoded_payload, str):
        return {'error': decoded_payload}, 400
    return {'payload': decoded_payload }

@app.errorhandler(404)
def page_not_found(error_str):
    return error_page()

# -------------

def app_onboard():
    return home_not_logged.app_onboard("home", "BrainBooks mining")

def app_dashboard(token):
    return dashboard.board(token)

def error_page():
    return  err.showError()

def mining_page(token):
    return mineria.mining_page(token)   

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
