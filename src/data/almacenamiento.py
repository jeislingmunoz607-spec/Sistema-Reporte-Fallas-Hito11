
reportes = [
    {
        "numero": "REP-024",
        "equipo": "PC-LAB02-07",
        "categoria": "Hardware",
        "descripcion": "La computadora no enciende",
        "estado": "Pendiente",
        "fecha": "03/11/2026",
        "solucion": ""
    },
    {
        "numero": "REP-023",
        "equipo": "PC-LAB01-12",
        "categoria": "Software",
        "descripcion": "El equipo presenta problemas al iniciar",
        "estado": "En proceso",
        "fecha": "02/11/2026",
        "solucion": ""
    },
    {
        "numero": "REP-022",
        "equipo": "PROY-LAB01",
        "categoria": "Conectividad",
        "descripcion": "Problemas de conexión",
        "estado": "Resuelto",
        "fecha": "01/11/2026",
        "solucion": "Se revisó la conexión del equipo"
    }
]


def obtener_reportes():
    return reportes


def buscar_reporte(numero):
    for reporte in reportes:
        if reporte["numero"] == numero:
            return reporte
    return None


def guardar_reporte(reporte):
    reportes.append(reporte)


def actualizar_solucion(numero, solucion):
    reporte = buscar_reporte(numero)

    if reporte:
        reporte["solucion"] = solucion
        reporte["estado"] = "Resuelto"
        return True

    return False
  
