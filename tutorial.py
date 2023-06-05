"""
print("Hola mundo")
print("2")

# Soy un comentario

''' 
Comentario multilinea

'''

"""
#Comentario multilinea 2

"""


#Variables (no hace falta indicar el tipo)
texto = "Hola que tal"
num = 2


#Imprimir variables
print(num, texto)
print(f"Hola, tengo {num} amigos")


#Obtener de una entrada (input)
'''
nombre = input("¿Cuál es tu nombre?\n")
print(f"Tu nombre es {nombre}")
'''

#Condiciones
victorias = 33
if victorias==33:
    print("El nano es el mejor")
else:
    print("Francés el último")


#Funciones
def mostrarAltura():
    altura = int(input("¿Cuál es tu altura?\n"))

    if altura >= 170:
        print ("Eres más alto que Messi")
    else:
        print ("Eres un enano")


mostrarAltura()

#Return
def mostrarAltura(altura):
    
    if altura >= 170:
        resultado = "Eres más alto que Messi"
    else:
        resultado = "Eres un enano"
    return resultado

altura = int(input("¿Cuál es tu altura?\n"))
print(mostrarAltura(altura))

"""
#Listas
personas = ["Alba", "Sonia", "Maria"]
print(personas[0])

for persona in personas:
    print (persona)
    