import grafo
import sys
import math
CANT_MAX_PARAM = 2
ARCHIVO = 1


def crear_grafo_archivo(archivo):
    '''Esta funcion se encarga de cargar los archivos del grafo, primero recorre todos los vertices del archivo y guarda en un diccionario auxiliar el nro de 
    id como clave y el nombre del personaje como dato y guarda en el diccionario vertices el nombre como lcave y como dato crea otro diccionario para los 
    adyacentes.
       Después recorre todas las aristas y se fija en el diccionario auxiliar cual es el nombre del personaje con el nro de id obtenido y lo busca en el diccionario
       de vertices y le asigna a su diccionario de adyacentes la clave como el nombre del personaje que esta conectado (que también se busca en el dic_auxiliar)
       y como dato el peso de la arista  '''

    with open(archivo, "r") as archivo_lectura:
        
        linea = archivo_lectura.readline()
        linea = archivo_lectura.readline() #Hago esto para que arranque a leer desde la linea despues de *Vertices
        cont_vertices = 0
        vertices = {} #Este diccionario gaurda como clave el nombre del personaje y como valor un diccionario de sus adyacentes
        dic_auxiliar = {} #Este diccionario contiene el ID del personaje como clave y el nombre como valor

        while "*Arcs" not in linea:

            aux = linea.split('"')
            nro_id = aux[0].rstrip(' ')
            dic_auxiliar[nro_id] = aux[1]
            vertices[aux[1]] = {}
            cont_vertices += 1
            linea = archivo_lectura.readline()

        linea = archivo_lectura.readline() 
        cont_aristas = 0    
        while (linea):
            linea = linea.rstrip('\n')
            arista = linea.split(' ')
            vertices[dic_auxiliar[arista[0]]][dic_auxiliar[arista[1]]] = float(arista[2])
            vertices[dic_auxiliar[arista[1]]][dic_auxiliar[arista[0]]] = float(arista[2])
            cont_aristas += 1
            linea = archivo_lectura.readline()
        
    grafo_marvel = grafo.Grafo(vertices, False, cont_vertices, cont_aristas)
    return grafo_marvel


def similares(grafo_marvel, personaje, cantidad):
    '''Parametros:
        grafo.
        personaje: el vertice del cual se quieren los similares.
        cantidad: la cantidad de similares que se desea obtener.
    Imprime los 'cantidad' similares del vertice recibido por parametro'''
    recorrido = grafo_marvel.random_walk(5000, personaje, True)
    cant_rep_personajes = Counter(recorrido) #Devuelve un diccionario con los personajes que paso y cuantas veces paso por ese mismo
    similares = cant_rep_personajes.most_common(cantidad + 1) #Devuelve una lista en la que se guardan los personajes que mas se repitieron y cuantas veces lo hicieron.
                                                              # El 1 se suma por si dentro de los mas comunes esta el personaje que se le pide los similares  
    contador = 0
    posicion = 0
    while (contador != cantidad):
        if (similares[posicion][0] != personaje):
            print(similares[posicion][0])
            contador += 1
        posicion += 1       

    
def recomendar (grafo_marvel, personaje, cantidad):
    '''Recibe un grafo, un vertice(personaje), y la cantidad de recomendados que se queira obtener(cantidad).
    Imprime los 'cantidad' recomendados del vertice que se ingresó por parametro'''
    recorrido = grafo_marvel.random_walk(5000, personaje, True)
    cant_rep_personajes = Counter(recorrido)    
    similares = cant_rep_personajes.most_common()

    contador = 0
    posicion = 0
    adyacentes = grafo_marvel.adyacentes(personaje)
    while (contador != cantidad):
        if (similares[posicion][0] != personaje and not(similares[posicion][0] in adyacentes)):
            print(similares[posicion][0])
            contador += 1
        posicion += 1    

def camino(grafo_marvel, origen, destino):
    '''Recibe un grafo, un vertice de salida(origen), y uno de llegada(destino).
    Imprime el camino mas corto, en tiempo, para llegar de origen a destino. Este camino tiene en cuenta que
    es conveniente que se desplace por los vertices que tienen mayor peso en la arista que los conecta, ya que
    estos son los que mas se counican entre si'''
    recorrido = grafo_marvel.camino_minimo(origen, destino, True);
    for personaje in recorrido:
        if personaje == destino: print(personaje)
        else: print(personaje, '->', end = ' ')


def centralidad(grafo_marvel, cantidad):
    ''' Recibe un grafo y una cantidad que indica la cantidad de personajes centrales de la red que se van a mostrar.
    Para esto lo que se va a hacer es recorrer varias veces con random_walk desde vertices alearios y la cantidad de vertices que mas 
    se repitan van a ser los mas centrales'''
    recorrido = grafo_marvel.random_walk(10000, None, True)
    cant_rep_personajes = Counter(recorrido)    
    similares = cant_rep_personajes.most_common()

    contador = 0
    while (contador != cantidad):
        print(similares[contador][0])
        contador += 1
        


def distancias(grafo_marvel, vertice):
    '''Recibe un grafo, y un vertice.
    Para ese vértice imprime cuantos vértices tiene en cada nivel de adyacencia. Sus adyacentes directos forman el nivel 1,
    los adyacentes de estos últimos forman el nivel 2, etc'''
    (padre, orden) = grafo_marvel.bfs(vertice)
    niveles = {}
    for vertice in orden:
        if orden[vertice] == 0: continue
        if orden[vertice] not in niveles:
            niveles[orden[vertice]] = 1
        else:
            niveles[orden[vertice]] += 1

    for nivel in niveles:
        print("Distancia {}: {}".format(nivel, niveles[nivel]))

def estadisticas(grafo_marvel):
    '''Recibe un grafo, e imprime los siguientes valores estadísticos:
    cantidad de vertices, cantidad de aristas, densidad del grafo, promedio de los grados de los vertices, desviación estandar
    del grado de cada vertice.'''

    cant_vertices = len(grafo_marvel)
    cant_aristas = grafo_marvel.obtener_cantidad_aristas()
    cant_max_aristas = cant_vertices * (cant_vertices - 1) / 2
    print("Cantidad de vertices:", cant_vertices)
    print("Cantidad de aristas:", cant_aristas)
    print("Densidad:", cant_aristas / cant_max_aristas)
    acumulador = 0
    for vertice in grafo_marvel:
        #acumulador es para el promedio de los grados de los vértices
        acumulador += len(grafo_marvel.adyacentes(vertice))
    promedio_grados = acumulador / cant_vertices
    print("Promedio del grado de cada vertice:", promedio_grados)
    
    #Desviacion estandar
    sumatoria = 0
    for vertice in grafo_marvel:
        sumatoria += (len(grafo_marvel.adyacentes(vertice)) - promedio_grados)**2
    print("Desvío estandar del grado de cada vértice:", math.sqrt(sumatoria / (cant_vertices - 1)))

def comunidades(grafo_marvel):
    ''' Recibe un grafo y muestras las comunidades que se forman a partir de que tan parecidos son los vertices
    entre ellos. Para esto utiliza label propagation y después creo otro diccionario en el que pongo los labels como claves y 
    los vertices como dato para poder devolver las comunidades '''
    
    labels = label_propagation(grafo_marvel, 100)

    comunidades = {}
    lista_labels = labels.keys()
    for i in range(len(lista_labels)):
        if (not(labels[lista_labels[i]] in comunidades)):
            comunidades[labels[lista_labels[i]]] = []
            comunidades[labels[lista_labels[i]]].append(lista_labels[i]) 

        comunidades[labels[lista_labels[i]]].append(lista_labels[i])

    lista_comunidades = camunidades.keys()
    for i in range(len(lista_comunidades)):
        if(len(comunidades[lista.comunidades[i]]) > 4 or len(comunidades[lista_comunidades[i]]) < 1000)
            print("La cantidad de miembros de la comunidad es "len(comunidad[lista_comunidades[i]])"\n")
            print(comunidades[lista_comunidades[i]]"\n")        




def obtener_comando(cadena):
    comando = ""
    parametro1 = ""
    parametro2 = ""
    espacios = 0
    comas = 0
    for posicion, letra in enumerate(cadena):
        if letra != ' ' and espacios == 0: comando += letra
        elif espacios == 0 and letra == ' ': espacios = 1
        else:
            if(comas == 0 and letra != ','): parametro1 += letra
            elif(comas == 1 and letra != ','): parametro2 += letra
            elif letra == ',': comas += 1
    return (comando, parametro1, parametro2.lstrip())

def main():
    cant_parametros = len(sys.argv)
    if(cant_parametros != CANT_MAX_PARAM):
        raise ValueError("No se ingreso la cantidad de parametros correcta")
    archivo = sys.argv[ARCHIVO]    
    grafo_marvel = crear_grafo_archivo(archivo)
    while(True):
        comando = input("")
        if comando == '': break  
        comandos = obtener_comando(comando)
        if comandos[0] == "similares": similares(grafo_marvel, comandos[1], int(comandos[2]))
        elif comandos[0] == "recomendar": recomendar(grafo_marvel, comandos[1], int(comandos[2]))
        elif comandos[0] == "camino": camino(grafo_marvel, comandos[1], comandos[2])
        elif comandos[0] == "distancias": distancias(grafo_marvel, comandos[1])
        elif comandos[0] == "estadisticas": estadisticas(grafo_marvel)
        elif comandos[0] == "centralidad": centralidad(grafo_marvel, int(comandos[1]))
        elif comandos[0] == "comunidad": comunidad(grafo_marvel)
        print('\n')
    

main() 
