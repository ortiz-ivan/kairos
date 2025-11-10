from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify,
    flash,
    session,
    g,
)
from functools import wraps
from database import get_connection
from models.producto import (
    obtener_productos,
    agregar_producto,
    editar_producto,
    eliminar_producto,
    obtener_producto_por_id,
    obtener_producto_por_codigo,
)
from models.venta import registrar_venta, obtener_ventas, obtener_detalle_venta
from models.usuario import verificar_usuario, obtener_usuario_por_id
import json

app = Flask(__name__)
app.secret_key = "clave_secreta_para_flash"  # necesaria para mostrar mensajes flash

# ---------------------------
# AUTENTICACIÓN Y ROLES
# ---------------------------


@app.before_request
def cargar_usuario():
    g.usuario = None
    if "user_id" in session:
        g.usuario = obtener_usuario_por_id(session["user_id"])


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if g.usuario is None:
            flash("Debe iniciar sesión para acceder.", "error")
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated


def roles_requeridos(*roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if g.usuario is None or g.usuario["rol"] not in roles:
                flash("No tiene permisos para acceder a esta página.", "error")
                return redirect(url_for("index"))
            return f(*args, **kwargs)

        return decorated

    return decorator


# Middleware para verificar que el usuario sea admin
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if g.usuario is None or g.usuario["rol"] != "admin":
            flash("Acceso denegado: se requiere rol de administrador.", "error")
            return redirect(url_for("index"))
        return func(*args, **kwargs)

    return decorated_function


# ---------------------------
# RUTAS DE AUTENTICACIÓN
# ---------------------------


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        usuario = verificar_usuario(username, password)
        if usuario:
            session["user_id"] = usuario["id"]
            session["rol"] = usuario["rol"]
            flash("Bienvenido", "success")
            return redirect(url_for("index"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesión cerrada", "success")
    return redirect(url_for("login"))


# ---------------------------
# RUTAS PRINCIPALES
# ---------------------------


@app.route("/")
@login_required
def index():
    return redirect(url_for("agregar_venta_view"))


# ---------------------------
# RUTAS DE VENTAS
# ---------------------------


@app.route("/ventas/agregar", methods=["GET", "POST"])
@login_required
def agregar_venta_view():
    if request.method == "POST":
        productos_json = request.form.get("productos")
        if productos_json:
            try:
                productos_cantidades = json.loads(productos_json)
                if productos_cantidades:
                    exito = registrar_venta(productos_cantidades)
                    if exito:
                        flash("Venta registrada correctamente.", "success")
                    else:
                        flash(
                            "Error al registrar la venta. Verifique el stock o los datos.",
                            "error",
                        )
            except Exception as e:
                flash(f"Error procesando venta: {e}", "error")
        return redirect(url_for("agregar_venta_view"))
    return render_template("agregar_venta.html")


@app.route("/api/buscar_producto/<codigo_barras>", methods=["GET"])
@login_required
def buscar_producto(codigo_barras):
    producto = obtener_producto_por_codigo(codigo_barras)
    if producto:
        return jsonify({"success": True, "producto": producto})
    else:
        return jsonify({"success": False, "mensaje": "Producto no encontrado"})


@app.route("/ventas")
@login_required
def ventas():
    ventas_list = obtener_ventas()
    return render_template(
        "ventas.html", ventas=ventas_list, obtener_detalle_venta=obtener_detalle_venta
    )


# ---------------------------
# RUTAS DE PRODUCTOS
# ---------------------------


@app.route("/productos")
@login_required
def productos():
    productos_list = obtener_productos()
    return render_template("productos.html", productos=productos_list)


@app.route("/productos/agregar", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def agregar_producto_view():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        categoria = request.form["categoria"]
        codigo_barras = request.form["codigo_barras"]
        agregar_producto(nombre, precio, stock, categoria, codigo_barras)
        return redirect(url_for("productos"))
    return render_template("agregar_producto.html")


@app.route("/productos/editar/<int:producto_id>", methods=["GET", "POST"])
@login_required
@roles_requeridos("admin")
def editar_producto_view(producto_id):
    producto = obtener_producto_por_id(producto_id)
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = float(request.form["precio"])
        stock = int(request.form["stock"])
        categoria = request.form["categoria"]
        codigo_barras = request.form["codigo_barras"]
        editar_producto(producto_id, nombre, precio, stock, categoria, codigo_barras)
        return redirect(url_for("productos"))
    return render_template("editar_producto.html", producto=producto)


@app.route("/productos/eliminar/<int:producto_id>")
@login_required
@roles_requeridos("admin")
def eliminar_producto_view(producto_id):
    eliminar_producto(producto_id)
    return redirect(url_for("productos"))


# ---------------------------
# INVENTARIO
# ---------------------------


@app.route("/inventario")
@login_required
def inventario():
    productos_list = obtener_productos()
    stock_bajo = 5
    categorias = sorted({p["categoria"] for p in productos_list})
    return render_template(
        "inventario.html",
        productos=productos_list,
        stock_bajo=stock_bajo,
        categorias=categorias,
    )


@app.route("/api/sugerencias_producto")
@login_required
def sugerencias_producto():
    q = request.args.get("q", "")
    productos = obtener_productos()
    resultados = [
        {"id": p["id"], "codigo_barras": p["codigo_barras"], "nombre": p["nombre"]}
        for p in productos
        if q in p["codigo_barras"]
    ][:10]
    return jsonify(resultados)


# ---------------------------
# PANEL DE ADMINISTRACIÓN (CRUD DE USUARIOS)
# ---------------------------


@app.route("/admin/usuarios")
@admin_required
def admin_usuarios():
    conn = get_connection()
    usuarios = conn.execute("SELECT id, username, rol FROM usuarios").fetchall()
    conn.close()
    return render_template("admin_usuarios.html", usuarios=usuarios)


@app.route("/admin/usuarios/nuevo", methods=["GET", "POST"])
@admin_required
def admin_usuario_nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        username = request.form["username"]
        password = request.form["password"]
        rol = request.form["rol"]

        conn = get_connection()
        conn.execute(
            "INSERT INTO usuarios (nombre, username, password, rol) VALUES (?, ?, ?, ?)",
            (nombre, username, password, rol),
        )
        conn.commit()
        conn.close()
        flash("Usuario creado exitosamente.", "success")
        return redirect(url_for("admin_usuarios"))
    return render_template("admin_usuario_form.html", action="Crear", usuario=None)


@app.route("/admin/usuarios/editar/<int:id>", methods=["GET", "POST"])
@admin_required
def admin_usuario_editar(id):
    conn = get_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (id,)).fetchone()
    if not usuario:
        flash("Usuario no encontrado.", "error")
        return redirect(url_for("admin_usuarios"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        username = request.form["username"]
        password = request.form["password"]
        rol = request.form["rol"]

        conn.execute(
            "UPDATE usuarios SET nombre=?, username=?, password=?, rol=? WHERE id=?",
            (nombre, username, password, rol, id),
        )
        conn.commit()
        conn.close()
        flash("Usuario actualizado correctamente.", "success")
        return redirect(url_for("admin_usuarios"))

    conn.close()
    return render_template("admin_usuario_form.html", action="Editar", usuario=usuario)


@app.route("/admin/usuarios/eliminar/<int:id>", methods=["POST"])
@admin_required
def admin_usuario_eliminar(id):
    conn = get_connection()
    conn.execute("DELETE FROM usuarios WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Usuario eliminado correctamente.", "success")
    return redirect(url_for("admin_usuarios"))


# ---------------------------
# INICIO DE APP
# ---------------------------

if __name__ == "__main__":
    app.run(debug=True)
