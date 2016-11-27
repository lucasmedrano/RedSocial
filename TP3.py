import grafo#.py 


def Cargar_archivo_en_grafo():
    '''Esta funcion se encarga de cargar los archivos del grafo, primero recorre todos los vertices del archivo y guarda en un diccionario auxiliar el nro de 
    id como clave y el nombre del personaje como dato y guarda en el diccionario vertices el nombre como lcave y como dato crea otro diccionario para los 
    adyacentes.
       Después recorre todas las aristas y se fija en el diccionario auxiliar cual es el nombre del personaje con el nro de id obtenido y lo busca en el diccionario
       de vertices y le asigna a su diccionario de adyacentes la clave como el nombre del personaje que esta conectado (que también se busca en el dic_auxiliar)
       y como dato el peso de la arista  '''

    with open("marvel.pjk", "r") as archivo:
        
        linea = archivo.readline()
        linea = archivo.readline() #Hago esto para que arranque a leer desde la linea despues de *Vertices
        cont_vertices = 0
        vertices = {} #Este diccionario gaurda como clave el nombre del personaje y como valor un diccionario de sus adyacentes
        dic_auxiliar = {} #Este diccionario contiene el ID del personaje como clave y el nombre como valor

        while linea != "*Arcs"

            aux = linea.split('"')
            dic_auxiliar[aux.pop(0)] = aux[0]
            vertices[aux[0]] = {}
            cont_vertices =+ 1
            linea = archivo.readline()

        linea = archivo.readline() 
        cont_aristas = 0    
        while linea != '':
            arista = linea.split(' ')
            vertices[dic_auxiliar[arista[1]]][dic_auxiliar[arista[2]]] = arista[3]
            vertices[dic_auxiliar[arista[2]]][dic_auxiliar[arista[1]]] = arista[3]
            cont_aristas =+ 1
        
    grafo = Grafo(False, vertices, cont_vertices, cont_aristas)    


def main()

    Cargar_archivo_en_grafo()



main()  
