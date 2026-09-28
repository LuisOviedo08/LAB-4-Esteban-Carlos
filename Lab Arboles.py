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

#Crear main para probar las funciones
def main():
    #... Aqui puede agregar codigo para probar las funciones definidas arriba