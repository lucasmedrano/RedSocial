import grafo
import sys
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
            vertices[dic_auxiliar[arista[0]]][dic_auxiliar[arista[1]]] = arista[2]
            vertices[dic_auxiliar[arista[1]]][dic_auxiliar[arista[0]]] = arista[2]
            cont_aristas += 1
            linea = archivo_lectura.readline()
        
    grafo_marvel = grafo.Grafo(vertices, False, cont_vertices, cont_aristas)
    return grafo_marvel


def main():
    
    cant_parametros = len (sys.argv)
    if(cant_parametros != CANT_MAX_PARAM):
        raise ValueError("No se ingreso la cantidad de parametros correcto")

    archivo = sys.argv[ARCHIVO]    

    grafo = crear_grafo_archivo(archivo)


main()
