class NodoLibro:
    def __init__(self, codigo, titulo, disponibles):
        self.codigo = codigo
        self.titulo = titulo
        self.disponibles = disponibles
        self.izquierdo = None
        self.derecho = None


def insertar(raiz, codigo, titulo, disponibles):
    if raiz is None:
        return NodoLibro(codigo, titulo, disponibles)
    if codigo < raiz.codigo:
        raiz.izquierdo = insertar(raiz.izquierdo, codigo, titulo, disponibles)
    elif codigo > raiz.codigo:
        raiz.derecho = insertar(raiz.derecho, codigo, titulo, disponibles)
    else:
        raise ValueError(f'Codigo duplicado: {codigo}')
    return raiz


def cargar_catalogo(ruta):
    raiz = None
    with open(ruta, encoding='utf-8') as archivo:
        for numero, linea in enumerate(archivo, 1):
            if not linea.strip():
                continue
            partes = linea.strip().split('|')
            if len(partes) != 3:
                raise ValueError(f'Linea {numero} incorrecta')
            codigo, titulo, disponibles = partes
            if int(disponibles) < 0:
                raise ValueError(f'Inventario negativo en linea {numero}')
            raiz = insertar(raiz, int(codigo), titulo, int(disponibles))
    return raiz


def buscar(nodo, codigo):
    if nodo is None or nodo.codigo == codigo:
        return nodo
    if codigo < nodo.codigo:
        return buscar(nodo.izquierdo, codigo)
    return buscar(nodo.derecho, codigo)


def listado_inorden(nodo):
    if nodo is None:
        return []
    return (listado_inorden(nodo.izquierdo)
            + [(nodo.codigo, nodo.titulo, nodo.disponibles)]
            + listado_inorden(nodo.derecho))


def prestar(raiz, codigo):
    libro = buscar(raiz, codigo)
    if libro is None or libro.disponibles == 0:
        return False
    libro.disponibles -= 1
    return True


def devolver(raiz, codigo):
    libro = buscar(raiz, codigo)
    if libro is None:
        return False
    libro.disponibles += 1
    return True


def total_disponibles(nodo):
    if nodo is None:
        return 0
    return (nodo.disponibles
            + total_disponibles(nodo.izquierdo)
            + total_disponibles(nodo.derecho))


def bajo_inventario(nodo):
    if nodo is None:
        return []
    izquierda = bajo_inventario(nodo.izquierdo)
    actual = [nodo.codigo] if nodo.disponibles <= 1 else []
    derecha = bajo_inventario(nodo.derecho)
    return izquierda + actual + derecha


def procesar_movimientos(raiz, ruta):
    aceptados = rechazados = 0
    with open(ruta, encoding='utf-8') as archivo:
        for numero, linea in enumerate(archivo, 1):
            if not linea.strip():
                continue
            partes = linea.strip().split('|')
            if len(partes) != 2:
                raise ValueError(f'Linea {numero} incorrecta')
            codigo_texto, operacion = partes
            codigo = int(codigo_texto)
            if operacion == 'PRESTAMO':
                exito = prestar(raiz, codigo)
            elif operacion == 'DEVOLUCION':
                exito = devolver(raiz, codigo)
            else:
                raise ValueError(f'Operacion invalida en linea {numero}')
            if exito:
                aceptados += 1
            else:
                rechazados += 1
    return aceptados, rechazados

def main():
    #Prueba provicional de las funciones
    raiz = cargar_catalogo('catalogo_libros.txt')
    print(listado_inorden(raiz))
    print(buscar(raiz, 330).titulo)
    print(prestar(raiz, 330))
    print(devolver(raiz, 580))
    print(total_disponibles(raiz))
    print(bajo_inventario(raiz))

    raiz = cargar_catalogo('catalogo_libros.txt')
    print(procesar_movimientos(raiz, 'movimientos.txt'))


def main():
    print('PASO 0: COMPROBAR LOS ARCHIVOS')
    with open('catalogo_libros.txt', encoding='utf-8') as archivo:
        print('Primer libro:', archivo.readline().strip())
    with open('movimientos.txt', encoding='utf-8') as archivo:
        print('Primer movimiento:', archivo.readline().strip())

    print('\nPASO 1: CONSTRUIR EL ARBOL')
    raiz = cargar_catalogo('catalogo_libros.txt')
    print('Raiz:', raiz.codigo)
    print('Hijos de 260:', raiz.izquierdo.izquierdo.codigo,
          raiz.izquierdo.derecho.codigo)
    print('Hijos de 580:', raiz.derecho.izquierdo.codigo,
          raiz.derecho.derecho.codigo)

    print('\nPASO 2: CONSULTAR EL CATALOGO')
    print('Libro 330:', buscar(raiz, 330).titulo)
    print('Codigo 999 registrado:', buscar(raiz, 999) is not None)
    for libro in listado_inorden(raiz):
        print(libro)

    print('\nPASO 3: PRESTAMOS')
    print('Primer prestamo de 330:', prestar(raiz, 330))
    print('Segundo prestamo de 330:', prestar(raiz, 330))
    print('Tercer prestamo de 330:', prestar(raiz, 330))
    print('Prestamo de 999:', prestar(raiz, 999))
    print('Disponibles de 330:', buscar(raiz, 330).disponibles)

    print('\nPASO 4: DEVOLUCIONES')
    print('Devolucion de 580:', devolver(raiz, 580))
    print('Devolucion de 999:', devolver(raiz, 999))
    print('Disponibles de 580:', buscar(raiz, 580).disponibles)

    print('\nPASO 5: REPORTE DE EXISTENCIAS')
    for libro in listado_inorden(raiz):
        print(libro)
    print('Ejemplares disponibles:', total_disponibles(raiz))
    print('Codigos de bajo inventario:', bajo_inventario(raiz))

    print('\nPASO 6: INGRESAR EL LIBRO 520')
    raiz = insertar(raiz, 520, 'Seguridad informatica', 2)
    print('Ruta: 410 -> 580 -> 490 -> 520 (hijo derecho de 490)')
    print([codigo for codigo, _, _ in listado_inorden(raiz)])
    print('Ejemplares disponibles:', total_disponibles(raiz))

    print('\nPASO 7: PROCESAR MOVIMIENTOS EN OTRO ARBOL')
    # Volver a leer el archivo evita mezclar el lote con las pruebas manuales.
    raiz_lote = cargar_catalogo('catalogo_libros.txt')
    aceptados, rechazados = procesar_movimientos(raiz_lote, 'movimientos.txt')
    print('Aceptados:', aceptados, 'Rechazados:', rechazados)
    print('Existencias:', total_disponibles(raiz_lote))
    print('Bajo inventario:', bajo_inventario(raiz_lote))
    for libro in listado_inorden(raiz_lote):
        print(libro)

    print('\nPRUEBA 1: ARBOL VACIO')
    print('buscar(None, 410):', buscar(None, 410))
    print('listado_inorden(None):', listado_inorden(None))
    print('total_disponibles(None):', total_disponibles(None))
    print('bajo_inventario(None):', bajo_inventario(None))

    print('\nPRUEBA 2: CODIGO DUPLICADO')
    try:
        raiz = insertar(raiz, 520, 'Otro libro', 1)
    except ValueError as error:
        print(error)
    print('Total despues del intento duplicado:', total_disponibles(raiz))


if __name__ == '__main__':
    main()