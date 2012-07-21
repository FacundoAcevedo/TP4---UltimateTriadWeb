#!/usr/bin/env python
#encoding: utf-8

import csv , os
from random import shuffle , choice




#---------------------------Constantes-----------------------------------

# Estos identificadores se utilizan dentro del archivo de estilos
# Para indicar de quién es cada carta. Si se modifican, es necesario
# modificar la hoja de estilos.
ESTILOS = { 1: "amigo", 2: "enemigo" }

#-----------------------------Clases-------------------------------------

class Juego (object):
    """ Clase que modela el juego Ultimate Triad. 
        Contiene la logica del juego y mantiene el estado del mismo. 
    """
    
    def __init__(self, jugador1, jugador2):
        """ Crea un nuevo juego a partir de los jugadores 
            (instancias de la clase Jugador) recibidos. 
            El juego se construye pero no se inicia.
        """  
        self.jugador1 = jugador1
        self.jugador2 = jugador2
        self.estado = False #True si se inicio, False si no
        self.turno = choice([1,2])
    
    def iniciar_juego(self):
        """ Inicia el juego. """
        self.estado = True 
        self.tablerito = Tablero(self.jugador1, self.jugador2)
        self.mano_jugador1 = self.jugador1.obtener_mano()
        self.mano_jugador2 = self.jugador2.obtener_mano()
        
        
    def esta_activo(self):
        """ Devuelve True si el juego se encuentra iniciado. 
            False en caso contrario. """
        return self.estado
    
    def obtener_jugadores(self):
        """ Devuelve una tupla con los jugadores que forman parte de este juego. """
        return (self.jugador1, self.jugador2)
        
    def obtener_tablero(self):
        """ Devuelve el tablero del juego. """
        return self.tablerito
        
    def turno_de(self):
        """ Devuelve 1 si es el turno del jugador1 
            o 2 de ser el turno del jugador2. """
        if self.turno == 1:
            return 1
        else:
            return 2
        
    def jugar_carta(self, id_carta, posicion_tablero):
        """ El jugador actula juega una carta en la posicion dada.
            id_carta es la posicion de la carta en la mano del jugador.
            Al finalizar se avanza el turno, y en caso de terminar el 
            juego, se lo marca como inactivo.
        """

        if self.turno == 1: #turno del jugador1
            self._proceso_jugada_carta(self.mano_jugador1, id_carta, self.jugador1, posicion_tablero, turno_siguiente=2)
        else:
            self._proceso_jugada_carta(self.mano_jugador2, id_carta, self.jugador2, posicion_tablero, turno_siguiente=1)
    
    def _proceso_jugada_carta(self, mano_jugador, id_carta, jugador, posicion_tablero, turno_siguiente):
        """Se encarga de cambiar el turno. colocar la carta, y actualizar el mazo"""    
        carta_elegida = mano_jugador[id_carta]
        jugador.sacar_carta_mano(id_carta)
        #Se la pongo al tablero
        self.tablerito.colocar_carta(carta_elegida, posicion_tablero)
        if self.tablerito.esta_completo():
            self.estado = False
        self.turno = turno_siguiente#cambio el turno
                
                
    def obtener_ganador(self):
        """ Devuelve el jugador que gano el juego, en caso
            de que no haya terminado, devuelve None. """
        if self.tablerito.esta_completo():
            if self.jugador1.puntaje > self.jugador2.puntaje:
                print "\n *** %s ha ganado esta mano! ***" % self.jugador1.nombre
                return self.jugador1
            elif self.jugador1.puntaje < self.jugador2.puntaje:
                print "\n *** %s ha ganado esta mano! ***" % self.jugador2.nombre
                return self.jugador2
            elif self.tablerito.esta_completo() and (len(self.jugador1.obtener_mano()) == 0):
                return self.jugador1
            elif self.tablerito.esta_completo() and (len(self.jugador2.obtener_mano()) == 0):
                return self.jugador2
        
        return None
        
class Jugador (object): #HECHO
    """ Modela un jugador en el juego Ultimate Triad """

   
    def __init__(self, nombre, id_jugador, nombre_mazo, cartas):
        """ Crea un nuevo jugador con los atributos recibidos
            id_jugador corresponde al identificador de jugador en el juego.
            cartas es una lista con los nombres de las cartas del mazo"""
        
        #seteo las variables locales
        self.nombre = nombre
        self.identificador = id_jugador
        self.puntaje = 5
        self.nombre_mazo = nombre_mazo 
        self.cartas = cartas #LISTADO DE NOMBRE DE LAS CARTAS
        self.mano = []
        self._generar_mano(cartas) #genero la mano
        self.io = ""
        
        

    def _generar_mano(self, lista_cartas):
        """ Genera una mano en base a la lista de cartas
            pasada"""
        carta = ""    
        for id in range(5):
            id = self._carta_a_objeto(lista_cartas[id], self.identificador)
            self.mano.append(id)
        
    def set_puntaje(self, puntaje):

        self.puntaje += puntaje
        

    
    def get_puntaje(self):
        """Devuelve el puntaje (como cadena)"""
        return str(self.puntaje)
        
    def reset_puntaje(self):
        self.puntaje = 5
    
    def _carta_a_objeto(self, carta, id_jugador):
        """Devuelve un objeto carta, con la carta pasada"""
        atributos= []  
        self.io = IO_control()
        print self.io
        atributos = self.io.obtener_fuerza(carta)
        return Carta(carta, id_jugador, atributos)
            
            
    def obtener_nombre(self):
        """ Devuelve el nombre del jugador. """
        
        return self.nombre
        
    def obtener_nombre_mazo(self):
        """ Devuelve el nombre del mazo del jugador. """
        
        return self.nombre_mazo
        
    def obtener_mano(self):
        """ Devuelve una lista de python con las cartas de la mano. """

        
        return self.mano
        
    def sacar_carta_mano(self, posicion):
        """ Elimina una carta de la mano del jugador en la posicion
            dada, la cual se corresponde a una posicion de la lista
            que devuelve obtener_mano"""
            
        

        self.mano.pop(posicion)
       
    
class Carta(object): #HECHO
    """ Modela una carta en el juego, con un nombre, que es constante, 
        y un estilo que puede ir cambiando a lo largo del juego.
    """

    def __init__(self, nombre, estilo, atributos):
        """ Crea una nueva carta con el nombre y el estilo recibidos. """
        #seteo las variables locales
        self.nombre = nombre
        self.estilo = estilo
        self.posicion_adyacente = None
        self.dueno = estilo
        self.norte = atributos[1]
        self.sur = atributos[2]
        self.este = atributos[3]
        self.oeste = atributos[4]
        
        

    def get_fuerza(self,direccion):
        if direccion == "n":
            return self.norte
        elif direccion == "s":
            return self.sur
        elif direccion == "e":
            return self.este
        elif direccion == "o":
            return self.oeste
    
    def set_dueno(self, dueno):
        """Define al dueño de la carta"""
        #  @param dueño
        #  @return None
        self.dueno = dueno
        self.estilo = dueno
    
    def get_dueno(self):
        if self.dueno:
            return self.dueno
        
    def obtener_nombre(self):
        """ Devuelve el nombre de la carta. """
        
        return self.nombre
        
    def obtener_estilo(self):
        """ Devuelve el estilo de la carta. """
        
        return ESTILOS[self.estilo]
    
    def comparar(self, pos, tablerito, jugador1, jugador2):
        """compara una carta con todos sus adyacentes """

        direccion_nodo_adyacente = ""
        carta_rival = ""

        nodo_destino = tablerito.pos[pos]
        direccion_invertida={"n":"s", "s":"n", "e":"o", "o":"e"}
        for direccion_nodo_adyacente in nodo_destino.nodos_adyacentes.iterkeys(): #recorro las direcciones adyacentes
            pos_nodo_adyacente = nodo_destino.nodos_adyacentes.get(direccion_nodo_adyacente, None) # ES UN DICCIONARIO POR DIOS!!!
            
            
            if pos_nodo_adyacente:
                pos_nodo_adyacente = tablerito.pos[pos_nodo_adyacente]
                carta_rival = pos_nodo_adyacente.get_carta() #obtengo la carta del nodo
                carta_elegida = tablerito.pos[pos].get_carta()
            
            if carta_rival and pos_nodo_adyacente and carta_rival.dueno != carta_elegida.dueno :
                # Si hay una carta junto a la propia cuyo dueño es otro que el jugador:
                fza_rival= int(carta_rival.get_fuerza(direccion_invertida[direccion_nodo_adyacente]))
                fza_carta_elegida = int(carta_elegida.get_fuerza(direccion_nodo_adyacente))
                
                if fza_carta_elegida >= fza_rival and pos_nodo_adyacente.pos: #comparo los bordes
                    tablerito.pos[pos_nodo_adyacente.pos].carta.set_dueno(carta_elegida.dueno)
                    if jugador1.identificador == carta_elegida.dueno: #Cargo los puntos
                        carta_rival.set_dueno(jugador1.identificador)
                        jugador1.set_puntaje(+1)
                        jugador2.set_puntaje(-1)
                    else:
                        carta_rival.set_dueno(jugador2.identificador)
                        jugador2.set_puntaje(+1)
                        jugador1.set_puntaje(-1)


class Tablero(object): #HECHO
    """ Modela un tablero de 3x3 para el juego Ultimate Triad """
    
    def __init__(self, jugador1, jugador2):
        """ Crea un tablero vacio"""
        self.posiciones = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
        self.pos = {}
        self.pos["A1"] = Nodo("A1",{"e":"A2", "o": None, "n": None,"s":"B1"})
        self.pos["A2"] = Nodo("A2",{"e":"A3", "o": "A1", "n": None, "s":"B2"})
        self.pos["A3"] = Nodo("A3",{"e":None, "o" : "A2", "n": None,"s":"B3"})
        self.pos["B1"] = Nodo("B1",{"e":"B2", "o": None, "n": "A1","s":"C1"})
        self.pos["B2"] = Nodo("B2",{"e":"B3", "o": "B1", "n": "A2","s":"C2"})
        self.pos["B3"] = Nodo("B3",{"e":None, "o": "B2", "n": "A3","s":"C3"})
        self.pos["C1"] = Nodo("C1",{"e":"C2", "o": None, "n": "B1","s":None})
        self.pos["C2"] = Nodo("C2",{"e":"C3", "o": "C1", "n": "B2","s":None})
        self.pos["C3"] = Nodo("C3",{"e":None, "o": "C2", "n": "B3","s":None})
        
        self.nodo_destino = None
        self.direccion_nodo_adyacente = None
        self.nodo_aux = None
        self.jugador1 = jugador1
        self.jugador2 = jugador2
                        
    def colocar_carta(self, carta_elegida, posicion_destino): #Cambie posicion por posicion_destino
        """ Coloca en el tablero la carta recibida en la posicion indicada.
            Las posiciones validas son:            
            'A1' 'A2' 'A3'
            'B1' 'B2' 'B3'
            'C1' 'C2' 'C3'
        """
        
        self.nodo_destino = self.pos[posicion_destino] #obtengo el diccionario de adyacentes
        if (self.nodo_destino.get_carta()):# Verifica si ya hay una carta en nodoDestino
            raise ValueError ("Esa posicion ya esta ocupada")
        self.nodo_destino.set_carta(carta_elegida) #Pone la carta elegida en el destino elegido
        carta_elegida.comparar(posicion_destino, self, self.jugador1, self.jugador2) 

        
    def obtener_carta(self, posicion):
        """ Devuelve la carta jugada en la posicion indicada 
        o None si no hay una carta jugada en esa posicion. """
       
       
        return self.pos[posicion].get_carta()
        
    def esta_completo(self):
        """ Devuelve True si el tablero esta completo. False en caso contrario. """
        lleno = True # se transformara a False si hay alguna posicion vacia
        for posicion in self.posiciones:
            if self.pos[posicion].get_carta() == None:
                lleno = False #si todas las posiciones tienen una carta, entonces nunca se pone False
        return lleno
        
#CLASES AGREGADAS POR NOSOTROS

class IO_control(object):
    """Relacionado con al escritura/lectura de archivos"""
    def __init__(self):
        pass

        
            
    def obtener_fuerza(self, nombre_carta, ruta = "data/cartas.csv"): 
        """Obtiene una carta del archivo .csv de manera aleatorea o por 
        nombre"""

        #  @return  una Carta(objeto)
     
        #variables
        salir = False
        
        #Codigo
        try:
            handler = open(ruta)
            cant_cartas = len(handler.readlines())
            csv_cartas = csv.reader(open(ruta), delimiter = ";")
        except IOError:
            raise IOError("A ocurrido un error mientras se intentaba abrir el\
            archivo de cartas")
        
        
        try:
            while salir != True:

                for nombre, norte, sur, este, oeste in csv_cartas:
                   
                    
                    if  str(nombre.rsplit()) == str(nombre_carta.rsplit()) and nombre != None:  
                        print "ADENTRO!!!"
                        salir = True
                        atributos = []
                        atributos.append(nombre)
                        atributos.append(norte)
                        atributos.append(sur)
                        atributos.append(este)
                        atributos.append(oeste)
                        break
                    
            csv_cartas = csv.reader(open(ruta), delimiter = ";")
            #transformo el valor A en 10
            for indice, valor in enumerate(atributos):
                if valor == "A":
                    atributos[indice] = "10"
            

            return atributos
        except ValueError:
            print "Un error inesperado ah ocurrido al obtener una carta!"

class Nodo(object):
    def __init__(self,pos , nodos_adyacentes = None, carta = None):
        self.nodos_adyacentes = nodos_adyacentes
        self.carta = None
        self.pos = pos

    def set_carta(self, carta):
        '''Coloca la carta en el nodo'''
        self.carta = carta
        
    def get_carta(self):
        '''Devuelve la carta que tiene el nodo, si hay una carta en el nodo'''
        
        if self.carta != None:
            return self.carta
        else:
            return None
 
    def __str__(self):
        '''Si tiene carta devuelve la carta, sino, None'''
        if self.carta:
            return str(self.carta.__str__())
        


# ********************************************************************** #
# A partir de aca son clases ya implementadas que no tienen que modificar#
# ********************************************************************** #

import sqlite3

class Usuario(object):
    """ Modela un usuario en el sistema. Sus atributos son:

        * self.uid       - Identificador unico de usuario (entero)
        * self.nombre    - Nombre del usuario
        * self.passwd    - Clave del usuario
    """
    def __init__(self, uid, nombre, passwd):
        """ Crea un nuevo usuario, con el id, nombre y clave recibidos. """        
        self.uid = uid
        self.nombre = nombre
        self.passwd = passwd
        
    
class Backend(object):
    """ Modela la base principal de operaciones de la pagina.
        Permite crear y listar usuarios, asi como tambien jugadores.
    """
    # Constantes de rutas
    BASE = "."
    STATIC = os.path.join(BASE, "static")
    DATA = os.path.join(BASE, "data")
    CARTAS = os.path.join(DATA, "cartas.csv")
    USUARIOS = os.path.join(DATA, "usuarios.db")
    AVATARS = os.path.join(DATA, "avatars")
    DECKS = os.path.join(DATA, "decks")
 
    def __init__(self):
        """ Crea el backend """

        # Directorios necesarios
        self.crear_dir(self.DATA)
        self.crear_dir(self.AVATARS)
        self.crear_dir(self.DECKS)

        # Archivo con los datos de los usuarios
        self.initializar_db()

        # Datos relacionados a las partidas
        self.esperando = []
        self.partidas = {}
        self.partidas_usuarios = {}
        self.ultima_partida = 0

    # Manejo de archivos / directorios               
    def crear_dir(self, ruta):
        """ Si la ruta no existe, la crea; sino no hace nada. """
        if not os.path.exists(ruta):
            os.makedirs(ruta)

    def obtener_ruta_static(self, *args):
        """ Devuelve una ruta completa a un archivo dentro la carpeta de
            archivos estaticos"""
        return os.path.join(self.STATIC, *args)
        
    def obtener_ruta_avatar(self, *args):
        """ Devuelve una ruta completa a un archivo dentro la carpeta de
            archivos de avatars. """
        return os.path.join(self.AVATARS, *args)
        
    def obtener_ruta_cartas(self):
        """ Devuelve la ruta hacia el archivo de las cartas oficiales """
        return self.CARTAS
 
    # Base de datos de usuarios
    def initializar_db(self):
        """ Crea la base de datos en caso de que no exista. """

        # Si no existe el archivo, lo crea y crea la tabla
        if not os.path.exists(self.USUARIOS):
            self.cx = sqlite3.connect(self.USUARIOS)
            cu = self.cx.cursor()
            cu.execute("""
                CREATE TABLE Usuarios (
                    Id INTEGER PRIMARY KEY, 
                    Nombre TEXT,
                    Password TEXT
                ); """)
            self.cx.commit()

        # Si el archivo existe, simplemente inicia la conexion
        else:
            self.cx = sqlite3.connect(self.USUARIOS)
        
    def usuario(self, uid):
        """ Devuelve el usuario correspondiente al id dado, o None si no existe."""
        
        cu = self.cx.cursor()
        cu.execute(""" 
            SELECT Id, Nombre, Password
            FROM Usuarios
            WHERE Id = '%d';
            """ % uid)
        linea = cu.fetchone()

        if linea:
            return Usuario(linea[0], linea[1], linea[2])

        return None

    def nuevo_usuario(self, nombre, clave):
        """ Crea un nuevo usuario, devuelve su identificador, 
            o None si el nombre ya existe."""

        # Validacion: nombre y clave son obligatorios
        if not nombre or not clave:
            return None
        
        # Verificacion: el nombre no puede estar repetido
        cu = self.cx.cursor()
        cu.execute(""" 
            SELECT Id, Nombre, Password
            FROM Usuarios
            WHERE Nombre = '%s';
            """ % nombre)
        linea = cu.fetchone()
        # Si ya existe el usuario, devuelve None
        if linea:
            return None
       
        # Inserta el nuevo usuario
        cu.execute("""
            INSERT INTO Usuarios (Nombre, Password)
            VALUES ( '%s', '%s' )
            """ % (nombre, clave))
        uid = cu.lastrowid

        # Guarda los cambios
        self.cx.commit()

        # Crea un avatar vacio para el usuario
        self.avatar_vacio(nombre)

        return uid

    def usuarios(self):
        """ Devuelve la lista completa de usuarios. """
        resultado = []

        cu = self.cx.cursor()
        cu.execute(" SELECT Id, Nombre, Password FROM Usuarios ")
        linea = cu.fetchone()
        while linea:
            resultado.append(Usuario(linea[0], linea[1], linea[2]))
            linea = cu.fetchone()
        return resultado

    # Manejo de avatares
    def avatar_vacio(self, nombre):
        """ Lee un avatar por omision y lo guarda para este usuario. """
        try:
            contenido = open(os.path.join(self.STATIC, "blankUser.jpg") , "rb") 
            self.cambiar_avatar(nombre, contenido.read()) 
            contenido.close()
        except IOError:
            # En caso de error, guarda una foto vacia
            self.cambiar_avatar(nombre, None)

    def cambiar_avatar(self, nombre, contenido):
        """ Guarda la imagen en el directorio de avatars, en forma de un archivo .jpg """
        path_avatar = os.path.join(self.AVATARS, nombre + ".jpg")
        avatar = open(path_avatar,"wb")
        avatar.write(contenido)
        avatar.close()

    # Manejo de Mazos
    def guardar_mazo(self, nombre, contenido):
        """ Guarda el archivo de texto pasado en su correspondiente directorio
            en forma de un archivo .dck. contenido es un archivo abierto. """ 

        # Realiza las validaciones necesarias
        self.validar_mazo(contenido)

        # Una vez validado, guarda el mazo
        path_deck = os.path.join(self.DECKS, nombre + ".dck")
        deck = open(path_deck, "w")
        deck.write(contenido)
        deck.close()

    def validar_mazo(self, contenido):
        """ Verifica que las cartas ingresadas al mazo sean validas. """
        lineas = contenido.split("\n")
        oficiales = [ x[0] for x in self.obtener_cartas_oficiales() ]
        for carta in lineas[1:]:
            if carta.strip() and carta.strip() not in oficiales:
                raise ValueError(
                    "Mazo invalido. No se reconoce la carta: %s." % carta)

    def obtener_mazo(self, nombre):
        """ Devuelve la informacion del archivo .dck en forma de una lista de python
            El archivo es de la forma:
               Nombre Mazo
               carta
               carta
               ...
        """
        # Intenta abrir el archivo
        try:
            archivo = open(os.path.join(self.DECKS, nombre + ".dck"), "r")
        except IOError:
            return []

        # Lee el nombre y las cartas
        nombre = archivo.readline()
        cartas = archivo.readlines()
        archivo.close()

        # Devuelve el mazo
        return [nombre, cartas]

    def obtener_cartas_oficiales(self):
        """ Devuelve una lista con tuplas de la forma:
            ('nombreCarta',norte,sur,este,oeste).
            La lista tiene ordenadas las tuplas en base al nombre de carta"""
            
        resultado = []
        try:
            archivo_cartas = open( self.CARTAS ,'r')
        except IOError:
            raise IOError, 'Error al abrir el archivo de base de datos'
        lectorCSV = csv.reader(archivo_cartas, delimiter=';')
        for carta in lectorCSV:
            resultado.append((carta[0], carta[1], carta[2], carta[3], carta[4]))
        archivo_cartas.close()
        return resultado
         
    # Interaccion con la clase Juego 
    def usuario_esperando(self, nombre):
        """ Agrega un usuario a la lista de usuarios esperando para jugar. """
        if not nombre in self.esperando:
            self.esperando.append(nombre)

    def crear_jugador(self, nombre, identificador):
        """ Crea una nueva instancia de la clase jugador. """
        try:
            nombre_mazo, cartas = self.obtener_mazo(nombre)
        except (TypeError, ValueError):
            raise ValueError("No se pudo crear el mazo para %s" % nombre)

        return Jugador(nombre, identificador, nombre_mazo, cartas)

    def crear_partida(self, nombre1, nombre2):
        """ Crea una nueva partida para los usuarios indicados. """

        # Elimina el o los nombres si estaban esperando
        for nombre in nombre1, nombre2:
            if nombre in self.esperando:
                self.esperando.remove(nombre)

        # Crea los jugadores
        jugador1 = self.crear_jugador(nombre1, 1)
        jugador2 = self.crear_jugador(nombre2, 2)

        # Crea la partida
        partida = Juego(jugador1, jugador2)

        # Guarda la partida en los diccionarios
        self.ultima_partida += 1
        id_partida = self.ultima_partida
        self.partidas[id_partida] = partida
        for nombre in nombre1, nombre2:
            if nombre in self.partidas_usuarios:
                self.partidas_usuarios[nombre].append(id_partida)
            else:
                self.partidas_usuarios[nombre] = [id_partida]

        return id_partida

    def partida(self, id_partida):
        if id_partida in self.partidas:
            return self.partidas[id_partida]
        raise ValueError("La partida solicitada no existe")


