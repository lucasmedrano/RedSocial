import random

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0

class Arista:
    def __init__(self, (desde, hasta), peso):
        self.desde = desde
        self.hasta = hasta
        self.peso = peso

    def __lt__(self, otro):
        if(self.peso < otro.peso) return -1
        elif(self.peso > otro.peso) return 1
        return 0

class Conjunto:
    def __init__(self, lista_vertices):
        self.lsita_vertices = vertices

class Grafo(object):
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
    
    def __init__(self, es_dirigido = False, vertices, cantidad_vertices = 0, cantidad_aristas = 0):
        '''Crea el grafo. El parametro 'es_dirigido' indica si sera dirigido, o no.'''
        self.es_dirigido = es_dirigido
        #Diccionario que tendrá como claves a los nombres de los personajes, y como valor, otro diccionario. Este segundo diccionario tendrá los
        #adyacentes al vértice, y como dato, el peso de la relacion vertice->adyacente
        self.vertices = vertices
        #Numero entero, indica la cantidad de vertices que tiene el grafo. Opcional
        self.cantidad_vertices = cantidad_vertices
        #Numero entero, cantidad de aristas que tiene el grafo. Opcional
        self.cantidad_aristas = cantidad_aristas

    def __len__(self):
        '''Devuelve la cantidad de vertices del grafo'''
        return self.cantidad_vertices
    
    def __iter__(self):
        '''Devuelve un iterador de vertices, sin ningun tipo de relacion entre los consecutivos'''
        return iter(self.vertices)
    
    def keys(self):
        '''Devuelve una lista de nombres de vertices. Iterar sobre ellos es equivalente a iterar sobre el grafo.'''
        return self.vertices.keys()
    
    def __contains__(self, nombre):
        ''' Determina si el grafo contiene un vertice con el nombre indicado.'''
        '''Devuelve si lo contiene o no'''
        return(nombre in self.vertices.keys())
        
    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: nombres de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        #Si hasta o desde no pertenecen al grafo, se lanza un error
        if ((hasta or desde) not in self.vertices.keys()):
            raise KeyError("Alguno de los nombres ingresados no forma parte del grafo")
        
        self.vertices[desde][hasta] = peso #Se cambia el peso de la arista

        #Si no es dirigido, se cambia tambien el peso de la arista inversa
        if not(self.es_dirigido):
            self.vertices[hasta][desde] = peso
        self.cantidad_aristas += 1;
        
    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: nombres de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
           Si el grafo no es dirigido, se borrará la arista inversa.
        '''
        
        #Si desde o hasta no pertenecen al grafo, se lanza un KeyError
        if((desde or hasta) not in self.vetices.keys()):
            raise KeyError("Alguno de los nombres ingresados no forma parte del grafo")

        #Si la relacion no existe, se lanza un ValueError
        if(hasta not in self.vertices[desde].keys()):
            raise ValueError("La arista ingresada por parámetro no existe")

        #Elimino la arista Desde->Hasta
        self.vertices[desde].pop(hasta)

        #Si no es dirigido, se borra también la arista Hasta->Desde
        if not(self.es_dirigido):
            self.vertices[hasta].pop(desde)
        self.cantidad_aristas -= 1;
    
    def obtener_peso_arista(self, desde, hasta):
        '''Obtiene el peso de la arista que va desde el vertice 'desde', hasta el vertice 'hasta'. Parametros:
            - desde y hasta: nombre de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            En caso de no existir la union consultada, se devuelve None.
        '''
        #Si desde o hasta no pertenecen al grafo, se lanza un KeyError
        if((desde or hasta) not in self.vertices.keys()):
            raise KeyError("Alguno de los nombres ingresados no forma parte del grafo")
        #SI la arista no existe, se lanza un ValueError
        if(hasta not in self.vertices[desde].keys()):
            return None
        #Devuelve el peso
        return self.vertices[desde][hasta]
    
    def adyacentes(self, nombre):
        '''Devuelve una lista con los vertices (nombres) adyacentes al indicado. Si no existe el vertice, se lanzara KeyError'''
        #Si "nombre" no pertenece al grafo, se lanza un KeyError
        if(nombre not in self.vertices.keys()):
            raise KeyError("el nombre ingresado no forma parte del grafo")
        return self.vertices.keys()
    
    #Recibe grafo, y tipo que indica si es BFS o DFS, luego llama a las funciones _BFS o _DFS segun corresponda.
    def recorrido(grafo, tipo):
        ''' Recorre el grafo y dependiendo del tipo que se le pase por parámetro lo recorre de forma BFS o DFS.
            Devuelve dos diccionarios, uno llamado padre y otro orden que indican el orden de como se recorrio el grafo'''
        visitados = {} #diccionario
        padre = {}
        orden = {}
        for v in grafo:
            if v not in visitados:
                padre[v] = None
                orden[v] = 0
                if(tipo == "BFS"):
                    _bfs(grafo, v, visitados, padre, orden)
                if(tipo =="DFS"):
                    _dfs(grafo, v, visitados, padre, orden)
        return padre, orden

    def bfs(grafo):
        return recorrido(grafo, "BFS")

    def dfs(grafo):
        return recorrido(grafo, "DFS")

    def _bfs(self, inicio, visitados, padre, orden):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el nombre del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un nombre, cual es el nombre del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un nombre, cual es su orden en el recorrido BFS
        '''

        q = Cola()
        q.encolar(origen)
        visitados[origen] = True
        while len(cola) > 0:
        v = cola.desencolar()
        for w in grafo.adyacentes(v):
            if w not in visitados:
                visitados[w] = True
                padre[w] = v
                orden[w] = orden[v] + 1
                q.encolar(w)


        raise NotImplementedError()
    
    def _dfs(self, inicio, visitados, padre, orden):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        - visitar: una funcion cuya firma sea del tipo: 
                    visitar(v, padre, orden, extra) -> Boolean
                    Donde 'v' es el identificador del vertice actual, 
                    'padre' el diccionario de padres actualizado hasta el momento,
                    'orden' el diccionario de ordenes del recorrido actualizado hasta el momento, y 
                    'extra' un parametro extra que puede utilizar la funcion (cualquier elemento adicional que pueda servirle a la funcion a aplicar). 
                    La funcion aplicar devuelve True si se quiere continuar iterando, False en caso contrario.
            - extra: el parametro extra que se le pasara a la funcion 'visitar'
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un identificador, cual es el identificador del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un identificador, cual es su orden en el recorrido DFS
        '''
        visitados[v] = True
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padre[w] = v
                orden[w] = orden[v] + 1
                _dfs(grafo, w, visitados, padre, orden)
        
    def camino_minimo(self, origen, destino, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra, o bien
        A* en caso que la heuristica no sea nula. Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None. 
        '''
        raise NotImplementedError()
    
    def mst(self):
        '''Calcula el Arbol de Tendido Minimo (MST) para un grafo no dirigido. En caso de ser dirigido, lanza una excepcion.
        Devuelve: un nuevo grafo, con los mismos vertices que el original, pero en forma de MST.'''
        raise NotImplementedError()

    def vertice_aleatorio(pesos):
        ´''' Devuelve un vértice aleatorio de los adyacentes del vertice que se recibe '''
        #Pesos es un diccionario de pesos, clave vértice vecino, valor el peso. Acomodar a implementacion
        total = sum(pesos.values())
        rand = random.uniform(0, total)
        acum = 0
        for vertice, peso_arista in pesos.items():
            if acum + peso_arista >= rand:
                return vertice
            acum += peso_arista
    
    def random_walk(self, largo, origen = None, pesado = False):
        ''' Devuelve una lista con un recorrido aleatorio de grafo.
            Parametros:
                - largo: El largo del recorrido a realizar(numero entero)
                - origen: Vertice (nombre) por el que se debe comenzar el recorrido. Si origen = None, se comenzara por un vertice al azar.
                - pesado: indica si se tienen en cuenta los pesos de las aristas para determinar las probabilidades de movernos de un vertice a uno de sus vecinos (False = todo equiprobable). 
            Devuelve:
                Una lista con los vertices (nombres) recorridos, en el orden del recorrido. 
        '''
        
        recorrido = []
        if not(origen):
            origen = random.choise(self.vertices.keys())

        actual = origen #Creo auxiliar, que va a ser el actual que voy a ir corriento y agregando a la lista
        recorrido.append(actual)
        if not(pesado): #No se tienen en cuenta los pesos. Simplemente se elije al azar
            for i in range(largo):
                actual = random.choise(self.vertices[actual].keys()) #Elijo un vertice al azar entre todos los adyacentes
                recorrido.append(actual) #Lo agrego a la lista
        if(pesado):
            for i in range(largo):
                actual = vertice_aleatorio(self.vertices[actual])
                recorrido.append(actual)
            
        return recorrido




