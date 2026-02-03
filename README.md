# 👜 BagShop - Sistema de Gestión de Inventario de Bolsos

Este es un proyecto **monolítico** desarrollado con **FastAPI** para la gestión del inventario de una tienda de bolsos. Permite realizar operaciones CRUD completas utilizando **SQL directo** (sin ORM) y validaciones avanzadas con **Pydantic**.

## 🛠️ Tecnologías utilizadas

* **Backend:** FastAPI (Python 3.12+)
* **Frontend:** Jinja2 Templates, Bootstrap 5, Bootstrap Icons
* **Base de Datos:** MySQL (Sentencias SQL nativas)
* **Validación:** Pydantic
* **Servidor:** Uvicorn

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Preparar el entorno

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno (Windows)
.\venv\Scripts\activate

# Activar el entorno (Linux/Mac)
source venv/bin/activate

# Instalar todas las librerías necesarias
pip install -r requirements.txt
```

### 2. Configurar la Base de Datos

1. Accede a tu gestor de base de datos (phpMyAdmin, MySQL Workbench, DBeaver, etc.)

2. Importa y ejecuta el script situado en `docs/init_db.sql`

3. Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example`):

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=tienda_bolsos
DB_USER=user_bolsos
DB_PASSWORD=bolsos123
```

### 3. Lanzar la aplicación

```bash
# Ejecutar desde la carpeta raíz del proyecto
uvicorn app.main:app --reload
```

La aplicación estará disponible en: **http://127.0.0.1:8000**

---

## 📋 Características Principales

### Gestión de Inventario
- ✅ **Añadir nuevos bolsos** con información detallada
- ✅ **Editar bolsos existentes** con validaciones en tiempo real
- ✅ **Eliminar bolsos** del inventario con confirmación
- ✅ **Listar todos los bolsos** con vista de tabla ordenada

### Campos del Producto
- Nombre y marca del bolso
- Tipo (bolso de mano, bandolera, mochila, clutch, tote, riñonera)
- Material y color
- Precio y stock
- Talla (pequeño, mediano, grande, XL)
- Temporada (primavera/verano, otoño/invierno, todo el año)
- Descripción detallada
