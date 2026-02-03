from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, field_validator, ValidationError
from typing import Optional, List
from decimal import Decimal

# Importamos funciones de base de datos
from app.database import (
    fetch_all_bolsos,
    insert_bolso,
    delete_bolso,
    fetch_bolso_by_id,
    update_bolso
)

# --------------------------------------------------
# MODELOS Pydantic
# --------------------------------------------------

# Modelo base con validaciones comunes
class BolsoBase(BaseModel):
    nombre: str
    marca: str
    tipo: str
    material: str
    color: str
    precio: float
    stock: int
    descripcion: str
    talla: str
    temporada: str

    @field_validator("nombre", "marca", "material", "color", "descripcion")
    def validar_texto(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El campo no puede estar vacío")
        return v.strip()

    @field_validator("precio")
    def validar_precio(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        if v > 100000:
            raise ValueError("El precio no puede superar los 100,000€")
        return round(v, 2)

    @field_validator("stock")
    def validar_stock(cls, v: int) -> int:
        if v < 0:
            raise ValueError("El stock no puede ser negativo")
        return v

    @field_validator("tipo")
    def validar_tipo(cls, v: str) -> str:
        tipos_validos = ["bolso_mano", "bandolera", "mochila", "clutch", "tote", "riñonera"]
        if v not in tipos_validos:
            raise ValueError("Tipo de bolso no válido")
        return v

    @field_validator("talla")
    def validar_talla(cls, v: str) -> str:
        tallas_validas = ["pequeño", "mediano", "grande", "xl"]
        if v not in tallas_validas:
            raise ValueError("Talla no válida")
        return v

    @field_validator("temporada")
    def validar_temporada(cls, v: str) -> str:
        temporadas_validas = ["primavera_verano", "otoño_invierno", "todo_el_año"]
        if v not in temporadas_validas:
            raise ValueError("Temporada no válida")
        return v


class BolsoDB(BolsoBase):
    id: int


class BolsoCreate(BolsoBase):
    pass


class BolsoUpdate(BolsoBase):
    pass


# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(title="BagShop – Tienda de Bolsos")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Motor de plantillas
templates = Jinja2Templates(directory="app/templates")


# --------------------------------------------------
# UTILIDAD
# --------------------------------------------------
def map_rows_to_bolsos(rows: List[dict]) -> List[BolsoDB]:
    """
    Convierte las filas del SELECT * FROM bolsos (dict) 
    en objetos BolsoDB (sin validaciones estrictas para datos existentes).
    """
    return [BolsoDB(**row) for row in rows]


# --------------------------------------------------
# RUTAS
# --------------------------------------------------

# --- GET principal ---
@app.get("/", response_class=HTMLResponse)
def get_index(request: Request, msg: str = None):
    # 1️⃣ Obtenemos los datos desde MySQL
    rows = fetch_all_bolsos()

    # 2️⃣ Convertimos cada fila a Bolso (valida estructura)
    bolsos = map_rows_to_bolsos(rows)

    # Lógica para decidir qué mensaje mostrar
    mensaje_exito = None
    if msg == "success":
        mensaje_exito = "¡Bolso añadido con éxito!"
    elif msg == "updated":
        mensaje_exito = "¡Bolso actualizado correctamente!"
    elif msg == "deleted":
        mensaje_exito = "El bolso ha sido eliminado."

    # 3️⃣ Enviamos a la plantilla
    return templates.TemplateResponse(
        "pages/index.html",
        {
            "request": request,
            "bolsos": bolsos,
            "mensaje_exito": mensaje_exito,
            "msg": msg
        }
        
    )


# --- GET formulario nuevo bolso---
@app.get("/bolsos/nuevo", response_class=HTMLResponse)
def get_nuevo_bolso(request: Request):
    return templates.TemplateResponse(
        "pages/nuevo_bolso.html",
        {"request": request}
    )


# --- POST guardar nuevo bolso ---
@app.post("/bolsos/nuevo")
def post_nuevo_bolso(
    request: Request,
    nombre: str = Form(...),
    marca: str = Form(...),
    tipo: str = Form(...),
    material: str = Form(...),
    color: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    descripcion: str = Form(...),
    talla: str = Form(...),
    temporada: str = Form(...)
):
    try:
        # 1. Validamos los datos con Pydantic
        bolso = BolsoCreate(
            nombre=nombre,
            marca=marca,
            tipo=tipo,
            material=material,
            color=color,
            precio=precio,
            stock=stock,
            descripcion=descripcion,
            talla=talla,
            temporada=temporada
        )

        # 2. Insertamos en la base de datos MySQL
        insert_bolso(**bolso.model_dump())
        
        # 3. ÉXITO: Redirigimos al inicio con el parámetro de éxito en la URL
        return RedirectResponse(url="/?msg=success", status_code=303)

    except ValidationError as e:
        # ERROR: Si Pydantic detecta fallos, volvemos al formulario con la lista de errores
        errores = [err["msg"] for err in e.errors()]
        return templates.TemplateResponse(
            "pages/nuevo_bolso.html",
            {
                "request": request,
                "errores": errores
            },
            status_code=422
        )

# --- DELETE eliminar bolso ---
@app.delete("/bolsos/{bolso_id}")
def delete_bolso_endpoint(bolso_id: int):
    if not delete_bolso(bolso_id):
        raise HTTPException(status_code=404, detail="Bolso no encontrado")
    return JSONResponse({"mensaje": "Bolso eliminado"})


# --- GET formulario editar bolso ---
@app.get("/bolsos/editar/{bolso_id}", response_class=HTMLResponse)
def get_editar_bolso(request: Request, bolso_id: int):
    """
    Endpoint para mostrar el formulario de edición con datos precargados.
    """
    # Obtenemos los datos del bolso
    data = fetch_bolso_by_id(bolso_id)
    if not data:
        raise HTTPException(status_code=404, detail="Bolso no encontrado")
    
    # Convertimos a modelo BolsoDB para mostrar en formulario (sin validaciones)
    bolso = BolsoDB(**data)
    return templates.TemplateResponse(
        "pages/editar_bolso.html",
        {"request": request, "bolso": bolso}
    )


# --- POST actualizar bolso a través de su id ---
@app.post("/bolsos/editar/{bolso_id}")
def post_editar_bolso(
    request: Request,
    bolso_id: int,
    nombre: str = Form(...),
    marca: str = Form(...),
    tipo: str = Form(...),
    material: str = Form(...),
    color: str = Form(...),
    precio: float = Form(...),
    stock: int = Form(...),
    descripcion: str = Form(...),
    talla: str = Form(...),
    temporada: str = Form(...)
):
    try:
        bolso = BolsoUpdate(
            nombre=nombre,
            marca=marca,
            tipo=tipo,
            material=material,
            color=color,
            precio=precio,
            stock=stock,
            descripcion=descripcion,
            talla=talla,
            temporada=temporada
        )

        if not update_bolso(bolso_id, **bolso.model_dump()):
            raise HTTPException(status_code=404, detail="Bolso no encontrado")

        return RedirectResponse(url="/?msg=updated", status_code=303)

    except ValidationError as e:
        errores = [err["msg"] for err in e.errors()]
        bolso_temp = BolsoDB(id=bolso_id, **bolso.model_dump())
        return templates.TemplateResponse(
            "pages/editar_bolso.html",
            {
                "request": request,
                "bolso": bolso_temp,
                "errores": errores
            },
            status_code=422
        )
    
    except Exception as e:
        # Error crítico (Base de datos, servidor, etc.)
        print(f"Error inesperado: {e}") # Para que tú lo veas en la consola
        return RedirectResponse(url="/?msg=error", status_code=303)
