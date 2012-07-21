#!/usr/bin/env python
#encoding: utf-8
  
import os, sys, time, random
import xml.sax.saxutils as saxutils

import bottle
from bottle import get, route, request, response, redirect, validate, view, static_file, error

import backend

#
# Configuracion
#

class config:
    # tiempo de sesion en seconds
    session_time = 30 * 60
    # base path for the backend
    path = './data'
    # base path for the sessions
    session_path = './data/sessions'

#
# Global backend instance
#
be = backend.Backend()

#
# Manejador de Sesion
#
class Session:
    def __init__(self, path, sid, uid):
        self.path = path
        self.sid = sid
        self.uid = uid

    def touch(self):
        if os.path.exists(self.path):
            os.utime(self.path, None)
        else:
            open(self.path, 'w')

    def save(self):
        fd = open(self.path, 'w')
        fd.write(str(self.uid))

    def load(self):
        self.uid = int(open(self.path).read())

    def check_expiration(self):
        if time.time() - os.stat(self.path).st_mtime > \
                config.session_time:
            os.unlink(self.path)
            return False
        return True

class SessionManager:
    """A simple, file-backed, lazy session manager.
    It stores sessions on files, but avoids remembering and loading them
    when possible. Removal of expired sessions is made randomly on session
    queries."""
    def __init__(self):
        self.path = config.session_path
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        # note that it does not neccesarily hold *all* the sessions,
        # just the ones we loaded
        self.sessions = {}

    def random_clean(self):
        "Clean all of the expired sessions every once in a while."
        if random.random() < 0.1:
            # the load_all() cleans them as it loads
            self.load_all()

    def load_all(self):
        for fn in os.listdir(self.path):
            if not fn.startswith('sess-'):
                continue
            sid = fn[len('sess-'):]
            s = self.load_one(sid)
            if s.check_expiration():
                self.sessions[sid] = s

    def load_one(self, sid):
        # note: it must NOT check expiration
        s = Session(self.path + '/sess-' + sid, sid, -1)
        s.load()
        return s

    def new(self):
        "Creates a new session. Note it is not saved."
        self.random_clean()
        sid = '%d-%d' % (time.time(), random.randint(0, 1000000))
        return Session(self.path + '/sess-' + sid, sid, -1)

    def __contains__(self, sid):
        self.random_clean()

        # we do the lazy loading into self.sessions
        if '/' in sid or '.' in sid or '\0' in sid:
            return False

        if sid in self.sessions:
            s = self.sessions[sid]
            if not s.check_expiration():
                del self.sessions[sid]
                return False
            return True

        if os.path.exists(self.path + '/sess-' + sid):
            s = self.load_one(sid)
            if not s.check_expiration():
                return False
            self.sessions[sid] = s
            return True

        return False

    def __getitem__(self, sid):
        if sid not in self:
            raise KeyError
        # __contains__() does the lazy loading into session
        s = self.sessions[sid]
        s.touch()
        return s

sessions = SessionManager()


#
# Users
#
class AuthError (Exception):
    pass

# Caches for users id <-> names and id -> passwd
class users:
    by_id = {}
    by_name = {}
    passwds = {}
    last_refresh = 0

def refresh_users(force = False):
    # refresh at most every 5 seconds
    if not force or time.time() <= users.last_refresh + 5: ####
        return

    us = be.usuarios()
    for u in us:
        users.by_id[u.uid] = u.nombre
        users.by_name[u.nombre] = u.uid
        users.passwds[u.uid] = u.passwd
    users.last_refresh = time.time()

def id_usuario(name = ''):
    "Devuelve el id para el usuario dado, o el id del usuario logeado"
    refresh_users()
    if name:
        return users.by_name[name]
    else:
        if not logged_in():
            return -1
        return sessions[request.cookies['sid']].uid

def user_name(uid = -1):
    "Returns the name for the given user id, or the current one"
    refresh_users()
    if uid < 0:
        uid = id_usuario()

    return users.by_id.get(uid, None)

def logged_in():
    sid = request.cookies.get('sid', "")
    if sid in sessions:
        uid = sessions[request.cookies['sid']].uid
        return uid in users.by_id
    return False

def add_user_status(f):
    def dec(*args, **kwargs):
        result = f(*args, **kwargs)

        if isinstance(result, dict):
            result["user_status"] = {
                "logged_in": logged_in(),
                "current_username": user_name(),
                "current_user": be.usuario(id_usuario()),
            }
        return result

    return dec

#
#Paginas 
#

#Pagina Principal 
@route('/')
@view('root')
@add_user_status
def root():
    return {
           'base_url': base_url, 
           }

#Pagina Jugar
@route('/jugar/:pid', method="GET")
@view('jugar')
@add_user_status
def pagina_juego_get(pid):

    try:
        partida = be.partida(int(pid))
    except ValueError, e:
        redirect("/lobby")

    jugador1, jugador2 = partida.obtener_jugadores() 
    tablero = partida.obtener_tablero()
    turno_jugador = partida.turno_de()
    
    #Si hay un ganador
    nombre_ganador = ""
    ganador = partida.obtener_ganador()
    if ganador: 
        nombre_ganador = ganador.obtener_nombre()
    
    return {
            'base_url': base_url,
            'jugadores': [jugador1, jugador2],
            'tablero' : tablero,
            'turno_jugador' : turno_jugador,
            'ganador' : nombre_ganador,
            'id_partida': pid,
            }

# 
@route('/jugar/:pid', method="POST")
def pagina_juego_post(pid):
    posicion_tablero = request.forms.tablero
    if posicion_tablero:
        partida = be.partida(int(pid))
        carta = obtener_numero_carta(request.forms.keys())
        partida.jugar_carta(carta, posicion_tablero)
    redirect("/jugar/"+pid)
    
#Pagina para chequear el turno
@route('/turno/:pid', method="GET")
@view('turno')
@add_user_status
def pagina_turno_get(pid):

    partida = be.partida(int(pid))
    turno_jugador = partida.turno_de()
    
    #Si hay un ganador
    if partida.obtener_ganador():
        turno_jugador = 0
    
    return {
            'base_url': base_url,
            'turno_jugador' : turno_jugador,
            }
    
#Pagina De Cartas
@route('/cartas')
@view('cartas')
def pagina_cartas():
    lista_cartas = be.obtener_cartas_oficiales()
    return{
            'base_url': base_url,
            'cartas' : lista_cartas,
            }
            
#Pagina Lobby
@route('/lobby', method="GET")
@view('lobby')
@add_user_status
def pagina_lobby_get(error=""):
    return {
            'esperando': be.esperando,
            'partidas': be.partidas,
            'error' : error,
            'base_url': base_url,
            }
            
# Marcarse como esperando
@route('/lobby/esperar', method="POST")
@view('lobby')
@add_user_status
def esperar():
    if user_name():
        be.usuario_esperando(user_name())
        bottle.redirect("/lobby")
    
    return pagina_lobby_get("Debe ingresar al sistema para poder esperar para jugar")

# Esperando para jugar
@route('/lobby/esperando', method="GET")
@view('esperando')
@add_user_status
def pagina_lobby_get(error=""):
    return {
            'esperando': be.esperando,
            'partidas': be.partidas_usuarios,
            'error' : error,
            'base_url': base_url,
            }
             
@route('/lobby/unir', method="POST")
@view('lobby')
@add_user_status
def unir_a_partida():
    try:
        jugador = request.POST.allitems()[0][0]
        id_partida = be.crear_partida(jugador, user_name())
        be.partida(id_partida).iniciar_juego()
        bottle.redirect("/jugar/"+str(id_partida))
    except ValueError, e:
        return pagina_lobby_get("Error al crear la partida: " + str(e))
            
#Pagina Registrar
@route('/registrar', method="GET")
@view('registrar')
def pagina_registrar_get():
    return{
            'error' : "",
            'base_url': base_url,
            }
            
#Pagina Registrar
@route('/registrar', method="POST")
@view('registrar')
def pagina_registrar_post():
            
    if 'username' not in request.POST or request.POST['username'] == "":
        return { 'base_url': base_url,
                'error': 'Por favor, ingrese un nombre de usuario' }
    
    if 'passwd' not in request.POST or request.POST['passwd'] == "":
        return { 'base_url': base_url,
                'error': 'Por favor, ingrese una clave' }

    uid = be.nuevo_usuario(request.POST['username'],
                            request.POST['passwd'])
    if not uid:
        return { 'base_url': base_url,
                'error': 'El nombre ya existe' }

    ########            
    
    refresh_users(True)
    s = sessions.new()
    s.uid = uid
    s.save()
    response.set_cookie('sid', s.sid)
    bottle.redirect(base_url + '/usuario/' + str(uid))

#Pagina Usuario
@route('/usuario/:uid', method="GET")
@view('usuario')
@add_user_status
def pagina_usuario(uid):
    _usuario = be.usuario(int(uid))
    return {
            'base_url' : base_url,
            'usuario' : _usuario,
            'be':be,
            }
            
@route('/subir_avatar', method = 'POST')
def subir_avatar():

    try:
        contenido = request.POST.get('avatar').file.read()
    except:
        return "<p class='error'>Error en el archivo enviado</p>"
                
    be.cambiar_avatar(user_name(), contenido)
    bottle.redirect("/usuario/"+str(id_usuario()))
    
@route('/subir_mazo', method = 'POST')
def subir_mazo():
    try:
        contenido = request.POST.get('mazo').file.read()
    except:
        return "<p class='error'>Error en el archivo enviado</p>"
    
    try:
        be.guardar_mazo(user_name(), contenido)
        bottle.redirect("/usuario/"+str(id_usuario()))
    except ValueError, e:
        return "<p class='error'>"+str(e)+"</p>"
    except IOError:
        return "<p class='error'>No se pudo leer el archivo</p>"
    
#Pagina Mazo Usuario
@route('/usuario/:uid/mazo', method="GET")
@view('mazo')
@add_user_status
def pagina_mazo(uid):
    _usuario = be.usuario(int(uid))
    _nombre_mazo , _cartas_mazo = be.obtener_mazo(_usuario.nombre)
    return {
            'base_url' : base_url,
            'usuario' : _usuario,
            'be':be,
            'mazo': _nombre_mazo,
            'cartas' :_cartas_mazo,
            }    
    
#Pagina Login
@route('/login')
@view('login')
@add_user_status
def login():
    return { 'base_url': base_url,
             'error': '' }
    
@route('/login', method = 'POST')
@view('login')
@add_user_status
def login_post():
    if 'username' not in request.POST or request.POST['username'] == "":
        return { 'base_url': base_url,
                'error': 'Por favor, ingrese el usuario' }
    if 'passwd' not in request.POST or request.POST['passwd'] == "":
        return { 'base_url': base_url,
                'error': 'Por favor, ingrese la clave' }

    refresh_users(True)
    if request.POST['username'] not in users.by_name:
        return { 'base_url': base_url,
             'error': 'Usuario incorrecto' }

    uid = id_usuario(request.POST['username'])

    if request.POST['passwd'] != users.passwds[uid]:
        return { 'base_url': base_url,
             'error': 'Clave incorrecta' }

    s = sessions.new()
    s.uid = uid
    s.save()
    response.set_cookie('sid', s.sid)
    bottle.redirect(base_url + '/usuario/' + str(uid))
 
@route('/logout')
def logout():
    response.set_cookie('sid', '')
    bottle.redirect(base_url + '/')
 
#
#Paginas De Error
#
@error(404)
@view('error404')
def error404(error):
    return {
        'base_url': base_url, 
        }

# 
#Statics \\Hojas de estilos, imagenes y demas
#

@route('/static/:fname#.*#')
def static(fname):
    # This is safe, as bottle validates the absolute resulting path is
    # inside the root
    return bottle.static_file(fname, root = "static/")
    
@route('/avatars/:fname#.*#')
def static(fname):
    # This is safe, as bottle validates the absolute resulting path is
    # inside the root
    return bottle.static_file(fname, root = "data/avatars")
    
@get('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root = "static/")

#
#Funciones utiles
#
    
def obtener_numero_carta(claves):
    """Para solucionar el problema del valor
        submit en firefox se busca si existe
        la clave de la carta"""
        
    for x in range(5):
        if "carta"+str(x)+".x" in claves:
            return x

            
##
# Main
##

# Base URL and path for URLs
host = "localhost"
port = "8080"
urlpath = ""

if len(sys.argv) > 1:
    host = sys.argv[1]
if len(sys.argv) > 2:
    port = sys.argv[2]
if len(sys.argv) > 3:
    urlpath = sys.argv[3]

base_url = "http://%s:%s%s" % (host, port, urlpath)

# Server start
if 'GATEWAY_INTERFACE' in os.environ:
    bottle.debug(True)
    bottle.run(server = bottle.CGIServer, quiet = True , reloader=True)
else:
    bottle.debug(True)
    bottle.run(host = host, port = port , reloader=True)
    

