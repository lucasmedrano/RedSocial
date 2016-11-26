import grafo#.py 


def Cargar_archivo_en_grafo():

    archivo = open("marvel.pjk")
    
    linea = archivo.readline()
    linea = archivo.readline() #Hago esto para que arranque a leer desde la linea despues de *Vertices
    cont_vertices = 0
    vertices = {} #Este diccionario gaurda como clave el nombre del personaje y como valor un diccionario de sus adyacentes
    auxiliar = {} #Este diccionario contiene el ID del personaje como clave y el nombre como valor


    while linea != "*Arcs"

        
        cont_vertices = cont_vertices + 1
        linea = archivo.readline()


    cont_aristas = 0    

        
    grafo = Grafo(False, vertices, cont_vertices, cont_aristas)    


def main()

    Cargar_archivo_en_grafo()



main()  
