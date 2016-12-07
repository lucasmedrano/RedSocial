import random
import math
import heapq
from collections import Counter

visitar_nulo = lambda a,b,c,d: True
heuristica_nula = lambda actual,destino: 0

class Personaje:
    def __init__(self, nombre, distancia = math.inf):
        '''Nombre debe ser un string, y distancia un numero'''
        self.nombre = nombre
        self.distancia = distancia

    def __lt__(self, otro):
        return self.distancia < otro.distancia

    def __eq__(self, otro):
        return self.distancia == otro.distancia

    def __gt__(self, otro):
        return self.distancia > otro.distancia

    def cambiar_distancia(self, distancia_nueva):
        '''Permite cambiar la distancia del personaje. distancia_nueva debe ser un numero'''
        self.distancia = distancia_nueva

    def obtener_nombre(self):
        '''Devuelve el nombre de un personaje'''
        return self.nombre

class Arista:
    def __init__(self, desde, hasta, peso):
        '''desde y hasta deben ser vertices del grafo. peso debe ser un numero'''
        self.desde = desde
        self.hasta = hasta
        self.peso = peso

    def __lt__(self, otro):
        return self.peso < otro.peso

    def __eq__(self, otro):
        return self.peso == otro.peso

    def __gt__(self, otro):
        return self.peso > otro.peso

class Grafo():
    '''Clase que representa un grafo. El grafo puede ser dirigido, o no, y puede no indicarsele peso a las aristas
    (se comportara como peso = 1). Implementado como "diccionario de diccionarios"'''
    
    def __init__(self, vertices, es_dirigido = False, cantidad_vertices = 0, cantidad_aristas = 0):
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

    def obtener_cantidad_aristas(self):
        '''Devuelve la cantidad de aristas del grafo'''
        return self.cantidad_aristas
        
    def agregar_arista(self, desde, hasta, peso = 1):
        '''Agrega una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: nombres de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - Peso: valor de peso que toma la conexion. Si no se indica, valdra 1.
            Si el grafo es no-dirigido, tambien agregara la arista reciproca.
        '''
        if ((hasta or desde) not in self.vertices.keys()):
            raise KeyError("Alguno de los nombres ingresados no forma parte del grafo")
        
        self.vertices[desde][hasta] = peso

        if not(self.es_dirigido):
            self.vertices[hasta][desde] = peso
        self.cantidad_aristas =+ 1;
        
    def borrar_arista(self, desde, hasta):
        '''Borra una arista que conecta los vertices indicados. Parametros:
            - desde y hasta: nombres de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
           En caso de no existir la arista, se lanzara ValueError.
           Si el grafo no es dirigido, se borrará la arista inversa.
        '''

        if((desde or hasta) not in self.vetices.keys()):
            raise KeyError("Alguno de los nombres ingresados no forma parte del grafo")

        if(hasta not in self.vertices[desde].keys()):
            raise ValueError("La arista ingresada por parámetro no existe")

        self.vertices[desde].pop(hasta)

        if not(self.es_dirigido):
            self.vertices[hasta].pop(desde)
        self.cantidad_aristas =- 1;
    
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
        return self.vertices[nombre].keys()
    
    def recorrido(self, tipo, inicio = None):
        ''' Recorre el grafo y dependiendo del tipo (BFS o DFS) que se le pase por parámetro lo recorre de forma BFS o DFS.
        Devuelve dos diccionarios, uno llamado padre y otro orden que permiten conocer el orden en el cual se recorrio el grafo, 
        y los ordenes de los vertices'''
        visitados = {}
        padre = {}
        orden = {}
        if not inicio:
            for v in self.vertices.keys():
                if v not in visitados:
                    padre[v] = None
                    orden[v] = 0
                    if(tipo == "BFS"): self._bfs(v, visitados, padre, orden)
                    if(tipo == "DFS"): self._dfs(v, visitados, padre, orden)
        else:
            for v in self.vertices.keys():
                padre[v] = None
                orden[v] = 0
            if(tipo == "BFS"): self._bfs(inicio, visitados, padre, orden)
            if(tipo == "DFS"): self._dfs(inicio, visitados, padre, orden)
        return padre, orden

    def bfs(self, inicio = None):
        '''Realiza un recorrido BFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un nombre, cual es el nombre del vertice padre en el recorrido BFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un nombre, cual es su orden en el recorrido BFS
        '''
        return self.recorrido("BFS", inicio)


    def _bfs(self, inicio, visitados, padre, orden):
        q = []
        q.append(inicio)
        visitados[inicio] = True
        while(len(q) > 0):
            v = q.pop(0)
            for w in self.adyacentes(v):
                if w not in visitados:
                    visitados[w] = True
                    padre[w] = v
                    orden[w] = orden[v] + 1
                    q.append(w)

    
    def dfs(self, inicio):
        '''Realiza un recorrido DFS dentro del grafo, aplicando la funcion pasada por parametro en cada vertice visitado.
        Parametros:
            - inicio: identificador del vertice que se usa como inicio. Si se indica un vertice, el recorrido se comenzara en dicho vertice, 
            y solo se seguira hasta donde se pueda (no se seguira con los vertices que falten visitar)
        Salida:
            Tupla (padre, orden), donde :
                - 'padre' es un diccionario que indica para un nombre, cual es el nombre del vertice padre en el recorrido DFS (None si es el inicio)
                - 'orden' es un diccionario que indica para un nombre, cual es su orden en el recorrido DFS
        '''
        return self.recorrido("DFS")

    def _dfs(self, inicio, visitados, padre, orden):
        visitados[v] = True
        for w in grafo.adyacentes(v):
            if w not in visitados:
                padre[w] = v
                orden[w] = orden[v] + 1
                self._dfs(w, visitados, padre, orden)
        
    def camino_minimo(self, origen, destino, inverso = False, heuristica=heuristica_nula):
        '''Devuelve el recorrido minimo desde el origen hasta el destino, aplicando el algoritmo de Dijkstra. 
        Parametros:
            - origen y destino: identificadores de vertices dentro del grafo. Si alguno de estos no existe dentro del grafo, lanzara KeyError.
            - heuristica: funcion que recibe dos parametros (un vertice y el destino) y nos devuelve la 'distancia' a tener en cuenta para ajustar los resultados y converger mas rapido.
            Por defecto, la funcion nula (devuelve 0 siempre)
        Devuelve:
            - Listado de vertices (identificadores) ordenado con el recorrido, incluyendo a los vertices de origen y destino. 
            En caso que no exista camino entre el origen y el destino, se devuelve None. 
        '''
        heap = []
        distancia = {}
        padre = {}
        visitados = {}

        for vertice in self.vertices.keys():
            distancia[vertice] = math.inf
            padre[vertice] = None
            visitados[vertice] = False

        personaje = Personaje(origen, 0)
        distancia[origen] = 0
        heapq.heappush(heap, personaje)

        while(heap):
            personaje = heapq.heappop(heap)
            vertice = personaje.obtener_nombre()
            visitados[vertice] = True

            for adyacente in self.adyacentes(vertice):
                if not inverso:
                    if (visitados[adyacente] == False) and (distancia[adyacente] > (distancia[vertice] + self.obtener_peso_arista(vertice, adyacente))):
                        distancia[adyacente] = distancia[vertice] + self.obtener_peso_arista(vertice, adyacente)
                        padre[adyacente] = vertice
                        personaje = Personaje(adyacente, distancia[adyacente])
                        heapq.heappush(heap, personaje)
                else:
                    if (visitados[adyacente] == False) and (distancia[adyacente] > (distancia[vertice] + (1 / self.obtener_peso_arista(vertice, adyacente)))):
                        distancia[adyacente] = (distancia[vertice]) + (1 / self.obtener_peso_arista(vertice, adyacente))
                        padre[adyacente] = vertice
                        personaje = Personaje(adyacente, distancia[adyacente])
                        heapq.heappush(heap, personaje)
        return self.descubrir_camino(origen, destino, padre, distancia)

    def descubrir_camino(self, origen, destino, padre, distancia):
        '''Parametros:
            origen: vertice en el cual comienza el recorrido.
            destino: vertice final del recorrido.
            padre: un diccionario que indica el padre de cada vertice.
            distancua: un diccionario con la distancia de cada vertice'''
        camino_minimo = []
        vertice = destino
        camino_minimo.append(vertice)
        while(vertice != origen):
            camino_minimo.append(padre[vertice])
            vertice = padre[vertice]
        camino_minimo.reverse()
        return camino_minimo

    def vertice_aleatorio(self, pesos):
        ''' Devuelve un vértice aleatorio de los adyacentes del vertice que se recibe.
        pesos es un diccionario que para cada arista, tiene su peso'''
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
            origen = random.choice(list(self.vertices.keys()))

        actual = origen
        recorrido.append(actual)
        if not(pesado):
            for i in range(largo):
                actual = random.choice(list(self.vertices[actual].keys()))
                recorrido.append(actual)
        if(pesado):
            for i in range(largo):
                actual = self.vertice_aleatorio(self.vertices[actual])
                recorrido.append(actual)
            
        return recorrido


    def label_propagation(self, largo):
        ''' Devuelve un diccionario con los nombres de los vertices como clave y como dato su label. Para esto lo que se hace es
        primero recorrer los vertices y sus adyacentes y colocarles como label el adyacente mas pesado. Luego se itera segun el largo 
        ingresado y se van modificando los labels segun la cantidad de labels repetidos en los adyacentes de los vertices.
        Si no se ve ningún cambio en los labels corta y termina antes  '''

        labels = {}
        personajes = list(self.vertices.keys())
        for i in range(len(personajes)):
            adyacentes = list(self.vertices[personajes[i]].items())
            mayor = 0
            label = None
            for j in range(len(adyacentes)):
                if(adyacentes[j][1] > mayor):
                    mayor = adyacentes[j][1]
                    label = adyacentes[j][0]

            labels[personajes[i]] = label


        for i in range(largo):
            contador = 0
            for j in range(len(personajes)):
                adyacentes = list(self.vertices[personajes[j]].keys())
                labels_adyacentes = []
                for k in range(len(adyacentes)):
                    labels_adyacentes.append(labels[adyacentes[k]])

                cant_rep_labels = Counter(labels_adyacentes)    
                comunes = cant_rep_labels.most_common(1)
                if (labels[personajes[j]] != comunes[0]):
                    contador += 1
                    labels[personajes[j]] = comunes[0]
            if (contador == 0):   
                break     

        return labels        
