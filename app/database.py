from dotenv import load_dotenv, find_dotenv
import os
import mysql.connector
from typing import List, Dict, Any, cast
from mysql.connector.cursor import MySQLCursorDict  

# Carga .env desde la raíz
load_dotenv(find_dotenv())

#conexión a la base de datos
def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),        
        user=os.getenv("DB_USER", "user_bolsos"),
        password=os.getenv("DB_PASSWORD", "bolsos123"),
        database=os.getenv("DB_NAME", "tienda_bolsos"),
        port=int(os.getenv("DB_PORT", "3306")),
        charset="utf8mb4"
    )

def fetch_all_bolsos() -> List[Dict[str, Any]]:
    """
    Obtiene todos los bolsos.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute("SELECT * FROM bolsos ORDER BY nombre")
            rows = cast(List[Dict[str, Any]], cur.fetchall())
            return rows
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

#insertar bolso
def insert_bolso(
    nombre: str,
    marca: str,
    tipo: str,
    material: str,
    color: str,
    precio: float,
    stock: int,
    descripcion: str,
    talla: str,
    temporada: str
) -> int:
    """
    Inserta un nuevo bolso y devuelve su ID.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                INSERT INTO bolsos
                (nombre, marca, tipo, material, color, precio, stock, descripcion, talla, temporada)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    nombre, marca, tipo, material, color, 
                    precio, stock, descripcion, talla, temporada
                )
            )
            conn.commit()
            return cur.lastrowid or 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()

def fetch_bolso_by_id(bolso_id: int) -> Dict[str, Any] | None:
    """
    Obtiene un bolso por su ID.
    Retorna un dict con los datos del bolso o None si no existe.
    """
    conn = None
    try:
        conn = get_connection()
        cur: MySQLCursorDict
        cur = conn.cursor(dictionary=True)  # type: ignore[assignment]
        try:
            cur.execute(
                "SELECT * FROM bolsos WHERE id = %s",
                (bolso_id,)
            )
            result = cur.fetchone()
            return dict(result) if result else None
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


# --------------------------------------------------
# DELETE: eliminar bolso
# --------------------------------------------------
def delete_bolso(bolso_id: int) -> bool:
    """
    Elimina un bolso de la base de datos por su ID.
    Retorna True si se eliminó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "DELETE FROM bolsos WHERE id = %s",
                (bolso_id,)
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()


# --------------------------------------------------
# UPDATE: actualizar bolso
# --------------------------------------------------
def update_bolso(
    bolso_id: int,
    nombre: str,
    marca: str,
    tipo: str,
    material: str,
    color: str,
    precio: float,
    stock: int,
    descripcion: str,
    talla: str,
    temporada: str
) -> bool:
    """
    Actualiza los datos de un bolso existente.
    Retorna True si se actualizó correctamente, False si no se encontró.
    """
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                """
                UPDATE bolsos
                SET nombre = %s,
                    marca = %s,
                    tipo = %s,
                    material = %s,
                    color = %s,
                    precio = %s,
                    stock = %s,
                    descripcion = %s,
                    talla = %s,
                    temporada = %s
                WHERE id = %s
                """,
                (
                    nombre, marca, tipo, material, color,
                    precio, stock, descripcion, talla, temporada,
                    bolso_id
                )
            )
            conn.commit()
            return cur.rowcount > 0
        finally:
            cur.close()
    finally:
        if conn:
            conn.close()
