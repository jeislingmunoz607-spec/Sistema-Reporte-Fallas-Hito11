
from data.almacenamiento import obtener_reportes, buscar_reporte, guardar_reporte, actualizar_solucion


def contar_reportes():
    reportes = obtener_reportes()

    pendientes = 0
    proceso = 0
    resueltos = 0

    for reporte in reportes:
        if reporte["estado"] == "Pendiente":
            pendientes += 1
        elif reporte["estado"] == "En proceso":
            proceso += 1
        else:
            resueltos += 1

    return pendientes, proceso, resueltos


def registrar_reporte(equipo, categoria, descripcion):
    reportes = obtener_reportes()

    numero = "REP-" + str(25 + len(reportes)).zfill(3)

    reporte = {
        "numero": numero,
        "equipo": equipo,
        "categoria": categoria,
        "descripcion": descripcion,
        "estado": "Pendiente",
        "fecha": "03/11/2026",
        "solucion": ""
    }

    guardar_reporte(reporte)

    return numero


def consultar_reportes(buscar="", estado=""):
    reportes = obtener_reportes()
    resultados = []

    for reporte in reportes:
        coincide_busqueda = (
            buscar.lower() in reporte["numero"].lower()
            or buscar.lower() in reporte["equipo"].lower()
        )

        coincide_estado = estado == "" or reporte["estado"] == estado

        if coincide_busqueda and coincide_estado:
            resultados.append(reporte)

    return resultados


def obtener_detalle(numero):
    return buscar_reporte(numero)


def registrar_solucion(numero, solucion):
    return actualizar_solucion(numero, solucion)
  
