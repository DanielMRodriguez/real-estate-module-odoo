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

Antes de levantar los contenedores, crea la carpeta `odoo-data`:

**Windows (PowerShell):**
```powershell
New-Item -ItemType Directory -Force -Path odoo-data
```

**Linux/Mac:**
```bash
mkdir -p odoo-data
```

Esta carpeta almacenará datos de sesión de Odoo. **Ya está incluida en el `.gitignore`** para no versionar los datos.

> **Nota para usuarios Linux/Mac**: Asegúrate de que el script `entrypoint.sh` tenga permisos de ejecución:
> ```bash
> chmod +x entrypoint.sh
> ```

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
- Odoo 17 (servidor web con inicialización automática)

**Primera ejecución**: El proceso tomará aproximadamente 1-2 minutos porque:
1. PostgreSQL inicializará su base de datos
2. El script `entrypoint.sh` detectará que es la primera vez
3. Inicializará automáticamente la base de datos `odoo` con el módulo `base`
4. Odoo quedará listo para usarse

Puedes monitorear el progreso con:
```bash
docker compose logs -f odoo
```

Busca el mensaje: `"Inicialización completada!"` para saber cuándo está listo.

### 5) Accede a Odoo

Abre tu navegador en:

```
http://localhost:8069
```

### 6) Usa la base de datos inicializada

Gracias a la inicialización automática, ya existe una base de datos llamada `odoo` lista para usar.

**Opción A - Usar la base de datos existente "odoo":**

En el navegador verás el login de Odoo. Crea tu usuario administrador:
1. **Email**: admin
2. **Password**: admin (cámbiala después)

**Opción B - Crear una nueva base de datos:**

Si prefieres crear una base de datos con otro nombre:
1. Ve a la pantalla de gestión de bases de datos
2. **Master password**: Por defecto es `admin`
3. Completa el formulario:
   - **Database Name**: `mi_base_datos`
   - **Email**: tu email
   - **Password**: contraseña del usuario admin
   - **Language**: Spanish / Español
   - **Country**: tu país
4. Haz clic en "Create database"

> **Nota**: La "Master Password" no es la contraseña de PostgreSQL, es una clave de seguridad para operaciones de administración de bases de datos desde el UI de Odoo.

---

## 📦 Estructura del proyecto

```
.
├── addons/              ← Aquí desarrollas tus módulos personalizados
│   └── empty_module/    (ejemplo de módulo vacío)
├── odoo-data/           ← Datos de sesión de Odoo (crear manualmente)
├── docker-compose.yml   ← Configuración de servicios Docker
├── entrypoint.sh        ← Script de inicialización automática de DB
├── Dockerfile           ← Para instalar dependencias Python (opcional)
├── .gitignore           ← Ignora odoo-data y otros archivos
└── readme.md            ← Este archivo
```

### ⚙️ Inicialización automática

El script `entrypoint.sh` se encarga de:
1. Esperar a que PostgreSQL esté disponible
2. Crear la base de datos `odoo` si no existe
3. Inicializar la base de datos con el módulo `base` en la primera ejecución
4. Iniciar Odoo normalmente

**Esto significa que no necesitas ejecutar comandos manuales en la primera vez.** Todo se configura automáticamente.

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

# Ver logs desde el inicio
docker compose logs odoo

# Detener servicios
docker compose down

# Eliminar todo (incluyendo volúmenes) - CUIDADO: Borra todas las bases de datos
docker compose down -v

# Reiniciar solo Odoo
docker compose restart odoo

# Acceder a la consola de Odoo
docker compose exec odoo bash

# Acceder a PostgreSQL
docker compose exec db psql -U odoo -d odoo
```

---

## 🔧 Solución de problemas

### Error: "Database odoo not initialized"

Este problema se soluciona automáticamente con el script `entrypoint.sh`. Si aún lo ves:

1. Verifica que el archivo `entrypoint.sh` exista en la raíz del proyecto
2. Reinicia los contenedores:
   ```bash
   docker compose down
   docker compose up -d
   ```
3. Monitorea los logs para ver el proceso de inicialización:
   ```bash
   docker compose logs -f odoo
   ```

### La inicialización toma mucho tiempo

En la primera ejecución, la inicialización del módulo `base` puede tomar 1-3 minutos. Esto es normal. Espera a ver el mensaje `"Inicialización completada!"` en los logs.

### Limpiar todo y empezar de cero

Si algo salió mal y quieres empezar completamente de cero:

**Windows (PowerShell):**
```powershell
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar carpeta de datos
Remove-Item -Recurse -Force odoo-data

# Crear de nuevo
New-Item -ItemType Directory -Force -Path odoo-data

# Levantar servicios
docker compose up -d
```

**Linux/Mac:**
```bash
# Detener y eliminar contenedores y volúmenes
docker compose down -v

# Eliminar carpeta de datos
rm -rf odoo-data

# Crear de nuevo
mkdir odoo-data

# Levantar servicios
docker compose up -d
```

### Forzar reinicialización manual de la base de datos

Si necesitas reinicializar manualmente la base de datos:

```bash
docker compose exec odoo odoo --db_host=db --db_user=odoo --db_password=odoo -d odoo -i base --stop-after-init
docker compose restart odoo
```

---

## 🤝 Contribuciones

Este es un template base. Siéntete libre de adaptarlo a tus necesidades y mejorarlo.

---

## 📄 Licencia

Este proyecto es de código abierto. Úsalo libremente para tus desarrollos.