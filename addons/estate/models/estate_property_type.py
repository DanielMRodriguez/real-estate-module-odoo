from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "id DESC"

    # =========================
    # Basic fields
    # =========================

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
   