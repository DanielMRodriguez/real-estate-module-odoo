#!/bin/bash
set -e

# Esperar a que PostgreSQL esté listo
echo "Esperando a que PostgreSQL esté disponible..."
until PGPASSWORD=$PASSWORD psql -h "$HOST" -U "$USER" -d postgres -c '\q' 2>/dev/null; do
  echo "PostgreSQL no está listo - esperando..."
  sleep 2
done

echo "PostgreSQL está listo!"

# Verificar si la base de datos 'odoo' existe
DB_EXISTS=$(PGPASSWORD=$PASSWORD psql -h "$HOST" -U "$USER" -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname='odoo'")

if [ "$DB_EXISTS" != "1" ]; then
  echo "Base de datos 'odoo' no existe. Creándola..."
  PGPASSWORD=$PASSWORD psql -h "$HOST" -U "$USER" -d postgres -c "CREATE DATABASE odoo OWNER odoo;"
fi

# Verificar si la base de datos está inicializada (checando si existe la tabla ir_module_module)
DB_INITIALIZED=$(PGPASSWORD=$PASSWORD psql -h "$HOST" -U "$USER" -d odoo -tAc "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'ir_module_module');" 2>/dev/null || echo "f")

if [ "$DB_INITIALIZED" = "f" ]; then
  echo "Base de datos 'odoo' no está inicializada. Inicializando con módulo base..."
  odoo --db_host="$HOST" --db_user="$USER" --db_password="$PASSWORD" -d odoo -i base --stop-after-init --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
  echo "Inicialización completada!"
else
  echo "Base de datos 'odoo' ya está inicializada."
fi

# Iniciar Odoo normalmente
echo "Iniciando Odoo..."
exec odoo --db_host="$HOST" --db_user="$USER" --db_password="$PASSWORD" --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons "$@"
