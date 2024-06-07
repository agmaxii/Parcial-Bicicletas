import csv
import random
import json
import os

def cargar_csv(nombre_archivo):
    """_summary_

    Args:
        nombre_archivo (_type_): _description_

    Returns:
        _type_: _description_
    """
    bicicletas = []
    if not os.path.isfile(nombre_archivo):
        print(f"El archivo {nombre_archivo} no se encontró.")
        return bicicletas
    
    try:
        with open(nombre_archivo, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                bicicletas.append({
                    'id_bike': int(row['id_bike']),
                    'nombre': row['nombre'],
                    'tipo': row['tipo'],
                    'tiempo': int(row['tiempo'])
                })
    except KeyError as e:
        print(f"El archivo CSV no contiene la columna esperada: {e}")
    except ValueError as e:
        print(f"Error al convertir los datos: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

    return bicicletas

def imprimir_lista(bicicletas):
    """_summary_

    Args:
        bicicletas (_type_): _description_
    """
    if not bicicletas:
        print("La lista de bicicletas está vacía.")
        return

    for bicicleta in bicicletas:
        print(bicicleta)

def asignar_tiempos(bicicletas):
    """_summary_

    Args:
        bicicletas (_type_): _description_

    Returns:
        _type_: _description_
    """
    for bicicleta in bicicletas:
        bicicleta['tiempo'] = random.randint(50, 120)
    return bicicletas

def informar_ganador(bicicletas):
    """_summary_

    Args:
        bicicletas (_type_): _description_

    Returns:
        _type_: _description_
    """
    if not bicicletas:
        print("No hay bicicletas en la lista.")
        return [], 0

    min_tiempo = bicicletas[0]['tiempo']
    ganadores = [bicicletas[0]['nombre']]
    for bicicleta in bicicletas[1:]:
        if bicicleta['tiempo'] < min_tiempo:
            min_tiempo = bicicleta['tiempo']
            ganadores = [bicicleta['nombre']]
        elif bicicleta['tiempo'] == min_tiempo:
            ganadores.append(bicicleta['nombre'])
    
    return ganadores, min_tiempo

def filtrar_por_tipo(bicicletas, tipo_filtro):
    """_summary_

    Args:
        bicicletas (_type_): _description_
        tipo_filtro (_type_): _description_

    Returns:
        _type_: _description_
    """
    bicicletas_filtradas = [bicicleta for bicicleta in bicicletas if bicicleta['tipo'] == tipo_filtro]
    nombre_archivo = f"{tipo_filtro}.csv"
    with open(nombre_archivo, mode='w', newline='') as csvfile:
        fieldnames = ['id_bike', 'nombre', 'tipo', 'tiempo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for bicicleta in bicicletas_filtradas:
            writer.writerow(bicicleta)
    return nombre_archivo

def informar_promedio_por_tipo(bicicletas):
    """_summary_

    Args:
        bicicletas (_type_): _description_

    Returns:
        _type_: _description_
    """
    tipos = {}
    for bicicleta in bicicletas:
        tipo = bicicleta['tipo']
        if tipo not in tipos:
            tipos[tipo] = []
        tipos[tipo].append(bicicleta['tiempo'])
    
    promedios = {}
    for tipo, tiempos in tipos.items():
        total_tiempo = 0
        for tiempo in tiempos:
            total_tiempo += tiempo
        promedio = total_tiempo / len(tiempos) if tiempos else 0
        promedios[tipo] = promedio
    
    return promedios

def ordenar_bicicletas(bicicletas):
    """_summary_

    Args:
        bicicletas (_type_): _description_

    Returns:
        _type_: _description_
    """
    n = len(bicicletas)
    for i in range(n):
        for j in range(0, n-i-1):
            if (bicicletas[j]['tipo'] > bicicletas[j+1]['tipo']) or \
               (bicicletas[j]['tipo'] == bicicletas[j+1]['tipo'] and bicicletas[j]['tiempo'] > bicicletas[j+1]['tiempo']):
                bicicletas[j], bicicletas[j+1] = bicicletas[j+1], bicicletas[j]
    return bicicletas

def mostrar_posiciones(bicicletas):
    """_summary_

    Args:
        bicicletas (_type_): _description_

    Returns:
        _type_: _description_
    """
    bicicletas_ordenadas = ordenar_bicicletas(bicicletas)
    return bicicletas_ordenadas

def guardar_posiciones(bicicletas_ordenadas):
    """_summary_

    Args:
        bicicletas_ordenadas (_type_): _description_
    """
    with open('posiciones.json', 'w') as jsonfile:
        json.dump(bicicletas_ordenadas, jsonfile, indent=4)

def menu():
    """_summary_
    """

    bicicletas = []
    while True:
        print("\nMenú:")
        print("1) Cargar archivo .csv")
        print("2) Imprimir lista bicicletas")
        print("3) Asignar los tiempos")
        print("4) Informar el ganador")
        print("5) Filtrar por tipo")
        print("6) Informar promedio por tipo")
        print("7) Mostrar las posiciones")
        print("8) Guardar las posiciones")
        print("9) Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            nombre_archivo = input("Ingrese el nombre del archivo CSV: ")
            bicicletas = cargar_csv(nombre_archivo)
        elif opcion == '2':
            imprimir_lista(bicicletas)
        elif opcion == '3':
            bicicletas = asignar_tiempos(bicicletas)
            imprimir_lista(bicicletas)
        elif opcion == '4':
            ganadores, min_tiempo = informar_ganador(bicicletas)
            if ganadores:
                print(f"El/los ganador(es) con tiempo {min_tiempo} es/son: {', '.join(ganadores)}")
            else:
                print("No hay ganadores para informar.")
        elif opcion == '5':
            tipo_filtro = input("Ingrese el tipo de bicicleta a filtrar: ")
            nombre_archivo = filtrar_por_tipo(bicicletas, tipo_filtro)
            print(f"Archivo guardado como {nombre_archivo}")
        elif opcion == '6':
            promedios = informar_promedio_por_tipo(bicicletas)
            for tipo, promedio in promedios.items():
                print(f"Promedio de tiempo para {tipo}: {promedio:.2f} minutos")
        elif opcion == '7':
            bicicletas_ordenadas = mostrar_posiciones(bicicletas)
            imprimir_lista(bicicletas_ordenadas)
        elif opcion == '8':
            bicicletas_ordenadas = mostrar_posiciones(bicicletas)
            guardar_posiciones(bicicletas_ordenadas)
            print("Posiciones guardadas en posiciones.json")
        elif opcion == '9':
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu()
