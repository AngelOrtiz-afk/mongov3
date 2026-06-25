import os
import re
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)

try:
    print("Estableciendo conexión...⏳")
    client.admin.command("ping")
except Exception as e:
    print(f"❌ ERROR EN LA CONEXIÓN: {e}")
    exit(code=1)

print("Conexión establecida 😊")

# Base de datos
db = client["prueba3"]

# Colecciones
coleccion_eventos = db["eventos"]
coleccion_invitados = db["invitados"]


# ─────────────────────────────────────────────────────────────────────────────
# POBLAR BASE DE DATOS (solo si están vacías)
# ─────────────────────────────────────────────────────────────────────────────

def poblar_base_de_datos() -> None:
    """Inserta datos de ejemplo si las colecciones están vacías."""

    if coleccion_eventos.count_documents({}) == 0:
        coleccion_eventos.insert_many([
            {
                "_id": 1,
                "codigo": "EVT-001",
                "nombre": "Conferencia de Ciberseguridad 2026",
                "fecha": "2026-07-15T09:00:00Z",
                "lugar": "Centro de Convenciones, Santiago",
                "categoria": "Tecnología",
                "invitados": [
                    {"rut": "11.009.876-3", "confirmado": True},
                    {"rut": "11.019.752-6", "confirmado": True},
                    {"rut": "11.029.628-9", "confirmado": False},
                    {"rut": "11.039.504-2", "confirmado": True},
                ]
            },
            {
                "_id": 2,
                "codigo": "EVT-002",
                "nombre": "Seminario de Inteligencia Artificial",
                "fecha": "2026-08-20T14:00:00Z",
                "lugar": "Auditorio INACAP, Valparaíso",
                "categoria": "Académico",
                "invitados": [
                    {"rut": "11.049.380-5", "confirmado": True},
                    {"rut": "11.009.876-3", "confirmado": True},
                    {"rut": "11.059.217-1", "confirmado": True},
                ]
            },
            {
                "_id": 3,
                "codigo": "EVT-003",
                "nombre": "Workshop de Redes y Protocolos",
                "fecha": "2026-09-05T10:30:00Z",
                "lugar": "Sala de Capacitación, Concepción",
                "categoria": "Técnico",
                "invitados": [
                    {"rut": "11.019.752-6", "confirmado": False},
                    {"rut": "11.029.628-9", "confirmado": True},
                ]
            },
            {
                "_id": 4,
                "codigo": "EVT-004",
                "nombre": "Hackathon TI 2026",
                "fecha": "2026-10-12T08:00:00Z",
                "lugar": "Campus Digital, Santiago",
                "categoria": "Competencia",
                "invitados": [
                    {"rut": "11.039.504-2", "confirmado": True},
                    {"rut": "11.049.380-5", "confirmado": True},
                    {"rut": "11.059.217-1", "confirmado": True},
                    {"rut": "11.009.876-3", "confirmado": False},
                    {"rut": "11.019.752-6", "confirmado": True},
                ]
            },
            {
                "_id": 5,
                "codigo": "EVT-005",
                "nombre": "Jornada de Protección de Datos",
                "fecha": "2026-11-03T16:00:00Z",
                "lugar": "Hotel Intercontinental, Santiago",
                "categoria": "Legal",
                "invitados": [
                    {"rut": "11.029.628-9", "confirmado": True},
                ]
            },
        ])
        print("✅ Colección 'eventos' poblada.")

    if coleccion_invitados.count_documents({}) == 0:
        coleccion_invitados.insert_many([
            {
                "rut": "11.009.876-3",
                "nombre": "Camila Herrera",
                "correo": "camila.herrera@empresa.cl",
                "empresa": "EmpresaX",
                "estado": "bloqueado"
            },
            {
                "rut": "11.019.752-6",
                "nombre": "Carla Rojas",
                "correo": "carla.rojas@empresa.cl",
                "empresa": "BlueCom",
                "estado": "activo"
            },
            {
                "rut": "11.029.628-9",
                "nombre": "Luis Fernández",
                "correo": "luis.fernandez@contratista.cl",
                "empresa": "DataShield",
                "estado": "activo"
            },
            {
                "rut": "11.039.504-2",
                "nombre": "Ana Martínez",
                "correo": "ana.martinez@empresa.cl",
                "empresa": "Inacap",
                "estado": "activo"
            },
            {
                "rut": "11.049.380-5",
                "nombre": "Diego Pérez",
                "correo": "diego.perez@gmail.com",
                "empresa": "FreelancerTI",
                "estado": "activo"
            },
            {
                "rut": "11.059.217-1",
                "nombre": "Fernanda Núñez",
                "correo": "fnunez@universidad.cl",
                "empresa": "Universidad de Chile",
                "estado": "activo"
            },
        ])
        print("✅ Colección 'invitados' poblada.")


# ─────────────────────────────────────────────────────────────────────────────
# REQUERIMIENTO 1 – Listar todos los eventos (Filtros)
# ─────────────────────────────────────────────────────────────────────────────

def requerimiento_1_listar_eventos() -> None:
    """
    Lista todos los eventos mostrando: código, nombre, fecha, lugar y categoría.
    También permite filtrar por categoría o fecha con criterios específicos.
    """
    print("\n" + "═" * 60)
    print("📅  REQUERIMIENTO 1 – LISTADO DE EVENTOS")
    print("═" * 60)

    # Filtro: todos los eventos
    query = {}

    print("\n[1.1] Todos los eventos:")
    documentos = coleccion_eventos.find(query, {
        "codigo": 1, "nombre": 1, "fecha": 1, "lugar": 1, "categoria": 1
    })

    for doc in documentos:
        print(f"""
  Código    : {doc['codigo']}
  Nombre    : {doc['nombre']}
  Fecha     : {doc['fecha']}
  Lugar     : {doc['lugar']}
  Categoría : {doc['categoria']}
  {'-' * 40}""")

    # Filtro por categoría "Tecnología"
    print("\n[1.2] Eventos de categoría 'Tecnología':")
    query_categoria = {"categoria": "Tecnología"}
    for doc in coleccion_eventos.find(query_categoria, {"codigo": 1, "nombre": 1, "fecha": 1, "lugar": 1, "categoria": 1}):
        print(f"  → {doc['codigo']} | {doc['nombre']} | {doc['fecha']}")

    # Filtro: eventos a partir de agosto 2026
    print("\n[1.3] Eventos desde agosto de 2026 en adelante:")
    query_fecha = {"fecha": {"$gte": "2026-08-01T00:00:00Z"}}
    for doc in coleccion_eventos.find(query_fecha, {"codigo": 1, "nombre": 1, "fecha": 1}):
        print(f"  → {doc['codigo']} | {doc['nombre']} | {doc['fecha']}")


# ─────────────────────────────────────────────────────────────────────────────
# REQUERIMIENTO 2 – Listar invitados con expresiones regulares
# ─────────────────────────────────────────────────────────────────────────────

def requerimiento_2_listar_invitados() -> None:
    """
    Lista invitados filtrando por:
    - Nombre parcial (case-insensitive) ingresado por el usuario.
    - Dominio de correo (ej. @empresa.cl).
    """
    print("\n" + "═" * 60)
    print("👤  REQUERIMIENTO 2 – LISTADO DE INVITADOS CON REGEX")
    print("═" * 60)

    # 2.1 Buscar por nombre parcial (case-insensitive)
    nombre_buscar = input("\n  Ingrese nombre parcial a buscar (o Enter para omitir): ").strip()

    if nombre_buscar:
        query_nombre = {"nombre": {"$regex": nombre_buscar, "$options": "i"}}
        print(f"\n  Invitados cuyo nombre contiene '{nombre_buscar}':")
        resultados = list(coleccion_invitados.find(query_nombre))
        if resultados:
            for doc in resultados:
                print(f"  → RUT: {doc['rut']} | Nombre: {doc['nombre']} | Correo: {doc['correo']} | Estado: {doc['estado']}")
        else:
            print("  ⚠️  No se encontraron resultados.")
    else:
        print("  (búsqueda por nombre omitida)")

    # 2.2 Filtrar por dominio de correo
    dominio_buscar = input("\n  Ingrese dominio de correo a filtrar (ej: empresa.cl) o Enter para omitir: ").strip()

    if dominio_buscar:
        # Escapar el punto para que no sea tratado como comodín regex
        dominio_escapado = re.escape(dominio_buscar)
        query_dominio = {"correo": {"$regex": f"@{dominio_escapado}$", "$options": "i"}}
        print(f"\n  Invitados con correo del dominio '@{dominio_buscar}':")
        resultados = list(coleccion_invitados.find(query_dominio))
        if resultados:
            for doc in resultados:
                print(f"  → RUT: {doc['rut']} | Nombre: {doc['nombre']} | Correo: {doc['correo']}")
        else:
            print("  ⚠️  No se encontraron resultados.")
    else:
        print("  (búsqueda por dominio omitida)")

    # 2.3 Mostrar todos los invitados activos (estado activo)
    print("\n  Todos los invitados con estado 'activo':")
    query_activo = {"estado": {"$regex": "^activo$", "$options": "i"}}
    for doc in coleccion_invitados.find(query_activo):
        print(f"  → RUT: {doc['rut']} | Nombre: {doc['nombre']} | Empresa: {doc['empresa']}")


# ─────────────────────────────────────────────────────────────────────────────
# REQUERIMIENTO 3 – Validar acceso de invitado a evento ($lookup)
# ─────────────────────────────────────────────────────────────────────────────

def requerimiento_3_validar_acceso() -> None:
    """
    Valida si un invitado tiene acceso a un evento específico cruzando
    información entre las colecciones 'invitados' y 'eventos' con $lookup.
    """
    print("\n" + "═" * 60)
    print("🔐  REQUERIMIENTO 3 – VALIDACIÓN DE ACCESO A EVENTO")
    print("═" * 60)

    # Entrada del usuario con validación básica
    rut_input = input("\n  Ingrese el RUT del invitado (ej: 11.009.876-3): ").strip()
    codigo_evento = input("  Ingrese el código del evento (ej: EVT-001): ").strip()

    # Validación de formato RUT básica
    patron_rut = r"^\d{1,2}\.\d{3}\.\d{3}-[\dkK]$"
    if not re.match(patron_rut, rut_input):
        print("  ⚠️  Formato de RUT inválido. Use el formato: XX.XXX.XXX-X")
        return

    # Validación de formato código evento
    patron_codigo = r"^EVT-\d{3}$"
    if not re.match(patron_codigo, codigo_evento.upper()):
        print("  ⚠️  Formato de código inválido. Use el formato: EVT-XXX")
        return

    codigo_evento = codigo_evento.upper()

    # Pipeline $lookup: cruzar eventos con invitados
    pipeline = [
        {
            "$match": {
                "codigo": codigo_evento,
                "invitados.rut": rut_input
            }
        },
        {
            "$lookup": {
                "from": "invitados",
                "localField": "invitados.rut",
                "foreignField": "rut",
                "as": "datos_invitados"
            }
        },
        {
            "$project": {
                "codigo": 1,
                "nombre": 1,
                "fecha": 1,
                "lugar": 1,
                "invitados": 1,
                "datos_invitados": {
                    "$filter": {
                        "input": "$datos_invitados",
                        "as": "inv",
                        "cond": {"$eq": ["$$inv.rut", rut_input]}
                    }
                }
            }
        }
    ]

    resultado = list(coleccion_eventos.aggregate(pipeline))

    if not resultado:
        print(f"\n  ❌ El invitado con RUT '{rut_input}' NO está registrado en el evento '{codigo_evento}'.")
        return

    evento = resultado[0]

    # Buscar estado de confirmación en el subdocumento
    confirmado = None
    for inv in evento.get("invitados", []):
        if inv["rut"] == rut_input:
            confirmado = inv["confirmado"]
            break

    # Obtener datos del invitado
    datos_inv = evento.get("datos_invitados", [{}])[0]

    # Verificar estado en colección invitados
    invitado_db = coleccion_invitados.find_one({"rut": rut_input})
    estado_invitado = invitado_db.get("estado", "desconocido") if invitado_db else "desconocido"

    print(f"""
  ✅ Invitado encontrado en el evento.

  ──── Datos del Invitado ────
  RUT     : {datos_inv.get('rut', rut_input)}
  Nombre  : {datos_inv.get('nombre', 'N/A')}
  Correo  : {datos_inv.get('correo', 'N/A')}
  Empresa : {datos_inv.get('empresa', 'N/A')}
  Estado  : {estado_invitado}

  ──── Datos del Evento ────
  Código  : {evento['codigo']}
  Nombre  : {evento['nombre']}
  Fecha   : {evento['fecha']}
  Lugar   : {evento['lugar']}

  ──── Resultado de Acceso ────""")

    if estado_invitado == "bloqueado":
        print("  🚫 ACCESO DENEGADO — El invitado está BLOQUEADO en el sistema.")
    elif confirmado:
        print("  ✅ ACCESO PERMITIDO — El invitado está CONFIRMADO para este evento.")
    else:
        print("  ⚠️  ACCESO PENDIENTE — El invitado NO ha confirmado asistencia.")


# ─────────────────────────────────────────────────────────────────────────────
# REQUERIMIENTO 4 – Top 3 eventos con más invitados confirmados (Agregación)
# ─────────────────────────────────────────────────────────────────────────────

def requerimiento_4_top3_eventos() -> None:
    """
    Obtiene el Top 3 de eventos con mayor cantidad de invitados confirmados
    usando un pipeline de agregación con $unwind, $match y $group.
    """
    print("\n" + "═" * 60)
    print("🏆  REQUERIMIENTO 4 – TOP 3 EVENTOS CON MÁS CONFIRMADOS")
    print("═" * 60)

    # Pipeline de agregación
    pipeline = [
        # Descomponer el array de invitados en documentos individuales
        {"$unwind": "$invitados"},
        # Filtrar solo los confirmados
        {"$match": {"invitados.confirmado": True}},
        # Agrupar por evento y contar confirmados
        {
            "$group": {
                "_id": "$_id",
                "codigo": {"$first": "$codigo"},
                "nombre": {"$first": "$nombre"},
                "fecha": {"$first": "$fecha"},
                "lugar": {"$first": "$lugar"},
                "categoria": {"$first": "$categoria"},
                "total_confirmados": {"$sum": 1}
            }
        },
        # Ordenar de mayor a menor
        {"$sort": {"total_confirmados": -1}},
        # Limitar a los 3 primeros
        {"$limit": 3}
    ]

    resultados = list(coleccion_eventos.aggregate(pipeline))

    if not resultados:
        print("\n  ⚠️  No hay datos disponibles.")
        return

    print()
    for posicion, doc in enumerate(resultados, start=1):
        medalla = ["🥇", "🥈", "🥉"][posicion - 1]
        print(f"  {medalla} #{posicion} — {doc['nombre']}")
        print(f"       Código     : {doc['codigo']}")
        print(f"       Categoría  : {doc['categoria']}")
        print(f"       Fecha      : {doc['fecha']}")
        print(f"       Lugar      : {doc['lugar']}")
        print(f"       Confirmados: {doc['total_confirmados']}")
        print()


# ─────────────────────────────────────────────────────────────────────────────
# MENÚ PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def mostrar_menu() -> None:
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║      SISTEMA DE GESTIÓN DE EVENTOS E INVITADOS          ║")
    print("║              Base de Datos: prueba3 (MongoDB)            ║")
    print("╠" + "═" * 58 + "╣")
    print("║  1. Listar todos los eventos (con filtros)               ║")
    print("║  2. Buscar invitados por nombre/dominio (regex)          ║")
    print("║  3. Validar acceso de invitado a evento ($lookup)        ║")
    print("║  4. Top 3 eventos con más confirmados (agregación)       ║")
    print("║  0. Salir                                                ║")
    print("╚" + "═" * 58 + "╝")


def main() -> None:
    poblar_base_de_datos()

    while True:
        mostrar_menu()
        opcion = input("\n  Seleccione una opción: ").strip()

        if opcion == "1":
            requerimiento_1_listar_eventos()
        elif opcion == "2":
            requerimiento_2_listar_invitados()
        elif opcion == "3":
            requerimiento_3_validar_acceso()
        elif opcion == "4":
            requerimiento_4_top3_eventos()
        elif opcion == "0":
            print("\n  👋 Hasta luego.\n")
            break
        else:
            print("\n  ⚠️  Opción inválida. Ingrese un número entre 0 y 4.")


if __name__ == "__main__":
    main()


