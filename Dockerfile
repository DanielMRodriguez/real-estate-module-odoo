FROM odoo:17

USER root

# Instala dependencias Python del repo de addons
COPY ./addons/requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

USER odoo
