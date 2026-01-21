# Odoo 17 Development Environment - Template Base

Este repositorio es una **plantilla base** para iniciar el desarrollo de módulos personalizados para Odoo 17.

Utiliza Docker para levantar un entorno de desarrollo completo con Odoo 17 y PostgreSQL 15, listo para que desarrolles tus propios addons en la carpeta `addons/`.

> **Nota**: Este repo está diseñado para ser descargado/clonado como punto de partida. Desarrolla tus módulos en tu propio repositorio usando esta base.

---

## 📋 Requisitos

- Docker Desktop (Windows/Mac) o Docker Engine (Linux)
- Docker Compose (incluido en Docker Desktop)
- Puertos libres:
  - `8069` (Odoo)
  - `5432` (Postgres) - *opcional exponerlo*

---

## 🚀 Instalación y configuración inicial

### 1) Descarga este repositorio como base

Puedes clonar este repo o descargarlo como ZIP para usarlo como plantilla:

```bash
git clone <URL_DE_ESTE_REPO> mi-proyecto-odoo
cd mi-proyecto-odoo
```

O si prefieres iniciar tu propio repositorio desde cero usando esta base:

```bash
# Descarga y elimina el historial git
git clone <URL_DE_ESTE_REPO> mi-proyecto-odoo
cd mi-proyecto-odoo
rm -rf .git
git init
```

### 2) Crea la carpeta de datos persistentes

Antes de levantar los contenedores, crea la carpeta `odoo-data` para almacenar los datos de PostgreSQL:

```bash
mkdir odoo-data
```

Esta carpeta almacenará la base de datos de forma persistente. **Ya está incluida en el `.gitignore`** para no versionar los datos.

### 3) (Opcional) Configura dependencias de Python

Si tus módulos requieren librerías de Python adicionales:

1. Crea un archivo `requirements.txt` dentro de la carpeta `addons/`
2. Modifica el `docker-compose.yml` para usar el Dockerfile en lugar de la imagen base:

**Cambia esto:**
```yaml
odoo:
  image: odoo:17
```

**Por esto:**
```yaml
odoo:
  build: .
  volumes:
    - ./addons:/mnt/extra-addons
```

El `Dockerfile` incluido en la raíz del proyecto está preparado para instalar las dependencias automáticamente.

### 4) Levanta los servicios

```bash
docker compose up -d
```

Esto iniciará:
- PostgreSQL 15 (base de datos)
- Odoo 17 (servidor web)

### 5) Accede a Odoo

Abre tu navegador en:

```
http://localhost:8069
```

### 6) Crea tu primera base de datos

En el navegador verás la pantalla de gestión de bases de datos:

1. **Master password**: Por defecto es `admin` (o la que definas en el contenedor)
2. Completa el formulario:
   - **Database Name**: `mi_base_datos`
   - **Email**: tu email
   - **Password**: contraseña del usuario admin
   - **Language**: Spanish / Español
   - **Country**: tu país
3. Haz clic en "Create database"

> **Nota**: La "Master Password" no es la contraseña de PostgreSQL, es una clave de seguridad para operaciones de administración de bases de datos desde el UI de Odoo.

---

## 📦 Estructura del proyecto

```
.
├── addons/              ← Aquí desarrollas tus módulos personalizados
│   └── empty_module/    (ejemplo de módulo vacío)
├── odoo-data/           ← Datos persistentes de PostgreSQL (crear manualmente)
├── docker-compose.yml   ← Configuración de servicios Docker
├── Dockerfile           ← Para instalar dependencias Python (opcional)
├── .gitignore           ← Ignora odoo-data y otros archivos
└── readme.md            ← Este archivo
```

---

## 🛠️ Desarrollo de módulos

### Crear un nuevo módulo

1. Crea una carpeta dentro de `addons/` con el nombre de tu módulo:
   ```bash
   mkdir addons/mi_modulo
   ```

2. Crea los archivos básicos:
   - `__init__.py`
   - `__manifest__.py`

3. Reinicia Odoo para que detecte el nuevo módulo:
   ```bash
   docker compose restart odoo
   ```

4. Actualiza la lista de aplicaciones en Odoo:
   - Ve a "Apps" → "Update Apps List"
   - Busca tu módulo e instálalo

### Aplicar cambios durante el desarrollo

Cuando hagas cambios en tu código:

```bash
# Reiniciar Odoo
docker compose restart odoo

# O si necesitas actualizar el módulo instalado
docker compose exec odoo odoo -u mi_modulo -d mi_base_datos --stop-after-init
```

---

## 🎯 Configuración avanzada

### Variables de entorno

Puedes crear un archivo `.env` para personalizar variables:

```env
ODOO_PORT=8069
POSTGRES_USER=odoo
POSTGRES_PASSWORD=odoo
POSTGRES_DB=postgres
```

### Addons path

El `docker-compose.yml` está configurado con:
- Addons del core de Odoo: `/usr/lib/python3/dist-packages/odoo/addons`
- Tus addons personalizados: `/mnt/extra-addons` (mapeado a `./addons`)

---

## 📝 Comandos útiles

```bash
# Ver logs de Odoo en tiempo real
docker compose logs -f odoo

# Detener servicios
docker compose down

# Eliminar todo (incluyendo volúmenes)
docker compose down -v

# Acceder a la consola de Odoo
docker compose exec odoo bash

# Acceder a PostgreSQL
docker compose exec db psql -U odoo
```

---

## 🤝 Contribuciones

Este es un template base. Siéntete libre de adaptarlo a tus necesidades y mejorarlo.

---

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para tus desarrollos.