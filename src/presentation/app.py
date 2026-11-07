
from flask import Flask, render_template_string, request, redirect, url_for, session

from business.logica import (
    contar_reportes,
    registrar_reporte,
    consultar_reportes,
    obtener_detalle,
    registrar_solucion
)

app = Flask(__name__)
app.secret_key = "sistema_fallas_unan"


estilo = """
<style>
* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #F3F6FA;
    color: #243247;
}

.contenedor {
    width: 100%;
    max-width: 1200px;
    min-height: 100vh;
    margin: auto;
    display: flex;
}

.menu {
    width: 240px;
    background: #123B70;
    color: white;
    padding: 24px 16px;
    flex-shrink: 0;
}

.logo {
    text-align: center;
    padding: 16px 8px;
    border-bottom: 1px solid #42618A;
    margin-bottom: 24px;
}

.logo h2 {
    font-size: 20px;
}

.logo p {
    font-size: 12px;
}

.menu a {
    display: block;
    color: white;
    text-decoration: none;
    padding: 14px 12px;
    margin-bottom: 8px;
    border-radius: 6px;
    font-size: 14px;
}

.menu a:hover {
    background: #28558C;
}

.contenido {
    flex: 1;
    min-width: 0;
    padding: 24px;
}

.encabezado {
    background: white;
    padding: 16px 24px;
    border-radius: 8px;
    margin-bottom: 24px;
    display: flex;
    justify-content: space-between;
    gap: 16px;
}

.encabezado h2 {
    margin: 0;
    color: #123B70;
}

.encabezado p {
    color: #66758A;
    font-size: 13px;
}

h1 {
    color: #123B70;
    font-size: 26px;
}

.subtitulo {
    color: #66758A;
    margin-bottom: 24px;
    font-size: 14px;
}

.tarjetas {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
}

.tarjeta, .panel {
    background: white;
    padding: 24px;
    border-radius: 8px;
    border: 1px solid #E1E7EF;
    margin-bottom: 24px;
}

.tarjeta h3 {
    font-size: 14px;
    color: #66758A;
}

.tarjeta strong {
    font-size: 28px;
    color: #123B70;
}

.panel h2 {
    color: #123B70;
    font-size: 19px;
}

button, .boton {
    height: 48px;
    padding: 0 20px;
    background: #15569A;
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
}

button:hover, .boton:hover {
    background: #0D3D70;
}

.boton-secundario {
    background: #E8EFF7;
    color: #123B70;
}

input, select, textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #C9D3E0;
    border-radius: 6px;
    margin-top: 8px;
    margin-bottom: 16px;
    font-size: 14px;
}

textarea {
    min-height: 110px;
}

label {
    font-size: 14px;
    font-weight: bold;
}

.tabla {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
}

.tabla th, .tabla td {
    padding: 14px 10px;
    border-bottom: 1px solid #E1E7EF;
    text-align: left;
}

.tabla th {
    color: #123B70;
    background: #F3F6FA;
}

.estado {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 20px;
    background: #E8EFF7;
    color: #123B70;
}

.mensaje {
    padding: 16px;
    background: #E1EEFF;
    border-radius: 6px;
    margin-bottom: 16px;
}

.login {
    width: 100%;
    max-width: 440px;
    margin: 70px auto;
    background: white;
    padding: 32px;
    border-radius: 10px;
}

.login h1, .login p {
    text-align: center;
}

.login button {
    width: 100%;
}

.pie {
    color: #77869A;
    font-size: 12px;
    text-align: center;
    margin-top: 24px;
}

@media (max-width: 750px) {
    .contenedor {
        display: block;
    }

    .menu {
        width: 100%;
        padding: 8px;
    }

    .logo {
        padding: 8px;
        margin-bottom: 8px;
    }

    .menu a {
        display: inline-block;
        padding: 12px 10px;
        margin: 2px;
        font-size: 12px;
    }

    .contenido {
        padding: 16px;
    }

    .tarjetas {
        grid-template-columns: 1fr;
    }

    .panel {
        overflow-x: auto;
    }

    .tabla {
        min-width: 560px;
    }

    .login {
        margin: 32px auto;
        padding: 24px;
    }
}
</style>
"""


menu = """
<div class="menu">
    <div class="logo">
        <h2>UNAN - LEÓN</h2>
        <p>Sistema de Reporte de Fallas</p>
        <p>CTIS25-SABE2-GP2</p>
    </div>

    <a href="/inicio">Inicio</a>
    <a href="/nuevo">Registrar falla</a>
    <a href="/consultar">Consultar reportes</a>
    <a href="/seguimiento">Seguimiento</a>
    <a href="/salir">Cerrar sesión</a>
</div>
"""


def pagina(titulo, contenido):
    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ titulo }}</title>
        {{ estilo|safe }}
    </head>
    <body>
        <div class="contenedor">
            {{ menu|safe }}

            <main class="contenido">
                <div class="encabezado">
                    <div>
                        <h2>UNAN - León</h2>
                        <p>Sistema de Reporte de Fallas de Computadoras</p>
                    </div>
                    <span>Grupo CTIS25-SABE2-GP2</span>
                </div>

                {{ contenido|safe }}

                <div class="pie">
                    Sistema de Reporte de Fallas - UNAN-León
                </div>
            </main>
        </div>
    </body>
    </html>
    """, titulo=titulo, contenido=contenido,
    estilo=estilo, menu=menu)


@app.route("/")
def principal():
    if "usuario" in session:
        return redirect(url_for("inicio"))

    return render_template_string("""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Acceso al sistema</title>
        {{ estilo|safe }}
    </head>
    <body>
        <div class="login">
            <h1>UNAN - LEÓN</h1>
            <p>Sistema de Reporte de Fallas de Computadoras</p>

            <form method="POST" action="/login">
                <label>Correo electrónico</label>
                <input type="email" name="correo" required>

                <label>Contraseña</label>
                <input type="password" name="contrasena" required>

                <button type="submit">Ingresar</button>
            </form>

            <p>Grupo CTIS25-SABE2-GP2</p>
        </div>
    </body>
    </html>
    """, estilo=estilo)


@app.route("/login", methods=["POST"])
def login():
    correo = request.form.get("correo")
    contrasena = request.form.get("contrasena")

    if correo and contrasena:
        session["usuario"] = correo
        return redirect(url_for("inicio"))

    return redirect(url_for("principal"))


@app.route("/inicio")
def inicio():
    if "usuario" not in session:
        return redirect(url_for("principal"))

    pendientes, proceso, resueltos = contar_reportes()

    contenido = """
    <h1>Tablero principal</h1>
    <p class="subtitulo">Resumen general de los reportes de fallas</p>

    <div class="tarjetas">
        <div class="tarjeta">
            <h3>Reportes pendientes</h3>
            <strong>""" + str(pendientes) + """</strong>
        </div>

        <div class="tarjeta">
            <h3>En proceso</h3>
            <strong>""" + str(proceso) + """</strong>
        </div>

        <div class="tarjeta">
            <h3>Reportes resueltos</h3>
            <strong>""" + str(resueltos) + """</strong>
        </div>
    </div>

    <div class="panel">
        <h2>Acciones principales</h2>
        <p>Desde este apartado puedes registrar una falla o consultar los reportes existentes.</p>
        <a class="boton" href="/nuevo">Registrar nueva falla</a>
        <a class="boton boton-secundario" href="/consultar">Consultar reportes</a>
    </div>
    """

    return pagina("Tablero principal", contenido)


@app.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if "usuario" not in session:
        return redirect(url_for("principal"))

    if request.method == "POST":
        equipo = request.form.get("equipo")
        categoria = request.form.get("categoria")
        descripcion = request.form.get("descripcion")

        numero = registrar_reporte(equipo, categoria, descripcion)

        return redirect(url_for("confirmacion", numero=numero))

    contenido = """
    <h1>Registrar una falla</h1>
    <p class="subtitulo">Completa los datos del equipo que presenta el problema</p>

    <div class="panel">
        <form method="POST">

            <label>Identificación del equipo</label>
            <input type="text" name="equipo" placeholder="Ejemplo: PC-LAB01-05" required>

            <label>Categoría de la falla</label>
            <select name="categoria" required>
                <option value="">Seleccionar categoría</option>
                <option>Hardware</option>
                <option>Software</option>
                <option>Conectividad</option>
                <option>Otro</option>
            </select>

            <label>Descripción del problema</label>
            <textarea name="descripcion" placeholder="Describe la falla que presenta el equipo" required></textarea>

            <button type="submit">Registrar reporte</button>
            <a class="boton boton-secundario" href="/inicio">Cancelar</a>

        </form>
    </div>
    """

    return pagina("Registrar falla", contenido)


@app.route("/confirmacion/<numero>")
def confirmacion(numero):
    if "usuario" not in session:
        return redirect(url_for("principal"))

    contenido = """
    <h1>Reporte registrado</h1>

    <div class="panel">
        <div class="mensaje">
            El reporte se registró correctamente.
        </div>

        <h2>Número de reporte: """ + numero + """</h2>

        <p>El estado inicial del reporte es Pendiente.</p>

        <a class="boton" href="/consultar">Ver reportes</a>
        <a class="boton boton-secundario" href="/inicio">Volver al tablero</a>
    </div>
    """

    return pagina("Confirmación", contenido)


@app.route("/consultar")
def consultar():
    if "usuario" not in session:
        return redirect(url_for("principal"))

    buscar = request.args.get("buscar", "")
    estado = request.args.get("estado", "")

    resultados = consultar_reportes(buscar, estado)

    filas = ""

    for reporte in resultados:
        filas += """
        <tr>
            <td>""" + reporte["numero"] + """</td>
            <td>""" + reporte["equipo"] + """</td>
            <td>""" + reporte["categoria"] + """</td>
            <td>""" + reporte["fecha"] + """</td>
            <td>""" + reporte["estado"] + """</td>
            <td><a href="/detalle/""" + reporte["numero"] + """">Ver</a></td>
        </tr>
        """

    if filas == "":
        filas = "<tr><td colspan='6'>No se encontraron reportes</td></tr>"

    contenido = """
    <h1>Consultar reportes</h1>
    <p class="subtitulo">Busca los reportes registrados en el sistema</p>

    <div class="panel">
        <form method="GET">
            <label>Buscar por número o equipo</label>
            <input type="text" name="buscar" placeholder="Ejemplo: REP-024 o PC-LAB02-07">

            <label>Filtrar por estado</label>
            <select name="estado">
                <option value="">Todos los estados</option>
                <option>Pendiente</option>
                <option>En proceso</option>
                <option>Resuelto</option>
            </select>

            <button type="submit">Buscar</button>
        </form>
    </div>

    <div class="panel">
        <h2>Lista de reportes</h2>

        <table class="tabla">
            <tr>
                <th>Número</th>
                <th>Equipo</th>
                <th>Categoría</th>
                <th>Fecha</th>
                <th>Estado</th>
                <th>Detalle</th>
            </tr>
            """ + filas + """
        </table>
    </div>
    """

    return pagina("Consultar reportes", contenido)


@app.route("/seguimiento")
def seguimiento():
    if "usuario" not in session:
        return redirect(url_for("principal"))

    reportes = consultar_reportes()
    filas = ""

    for reporte in reportes:
        filas += """
        <tr>
            <td>""" + reporte["numero"] + """</td>
            <td>""" + reporte["equipo"] + """</td>
            <td>""" + reporte["estado"] + """</td>
            <td><a href="/detalle/""" + reporte["numero"] + """">Consultar</a></td>
        </tr>
        """

    contenido = """
    <h1>Seguimiento de reportes</h1>
    <p class="subtitulo">Consulta el estado de atención de cada falla</p>

    <div class="panel">
        <table class="tabla">
            <tr>
                <th>Número</th>
                <th>Equipo</th>
                <th>Estado</th>
                <th>Acción</th>
            </tr>
            """ + filas + """
        </table>
    </div>
    """

    return pagina("Seguimiento", contenido)


@app.route("/detalle/<numero>")
def detalle(numero):
    if "usuario" not in session:
        return redirect(url_for("principal"))

    reporte = obtener_detalle(numero)

    if reporte:
        contenido = """
        <h1>Detalle del reporte</h1>

        <div class="panel">
            <h2>Información del equipo</h2>

            <p><strong>Número:</strong> """ + reporte["numero"] + """</p>
            <p><strong>Equipo:</strong> """ + reporte["equipo"] + """</p>
            <p><strong>Categoría:</strong> """ + reporte["categoria"] + """</p>
            <p><strong>Descripción:</strong> """ + reporte["descripcion"] + """</p>
            <p><strong>Fecha:</strong> """ + reporte["fecha"] + """</p>
            <p><strong>Estado:</strong> """ + reporte["estado"] + """</p>
            <p><strong>Solución:</strong> """ + (reporte["solucion"] or "Todavía no se ha registrado una solución") + """</p>

            <a class="boton" href="/solucion/""" + numero + """">Registrar solución</a>
            <a class="boton boton-secundario" href="/consultar">Volver</a>
        </div>
        """
    else:
        contenido = "<div class='panel'>No se encontró el reporte solicitado.</div>"

    return pagina("Detalle del reporte", contenido)


@app.route("/solucion/<numero>", methods=["GET", "POST"])
def solucion(numero):
    if "usuario" not in session:
        return redirect(url_for("principal"))

    reporte = obtener_detalle(numero)

    if not reporte:
        return pagina("Reporte no encontrado",
                      "<div class='panel'>No se encontró el reporte.</div>")

    if request.method == "POST":
        solucion = request.form.get("solucion")
        registrar_solucion(numero, solucion)

        return redirect(url_for("detalle", numero=numero))

    contenido = """
    <h1>Registrar solución</h1>
    <p class="subtitulo">Completa la información de atención de la falla</p>

    <div class="panel">
        <h2>Reporte: """ + numero + """</h2>

        <form method="POST">
            <label>Descripción de la solución</label>
            <textarea name="solucion" placeholder="Describe cómo se solucionó la falla" required></textarea>

            <button type="submit">Guardar solución</button>
            <a class="boton boton-secundario" href="/detalle/""" + numero + """">Cancelar</a>
        </form>
    </div>
    """

    return pagina("Registrar solución", contenido)


@app.route("/salir")
def salir():
    session.clear()
    return redirect(url_for("principal"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
      
