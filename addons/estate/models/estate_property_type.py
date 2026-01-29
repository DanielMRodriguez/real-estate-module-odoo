from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _order = "name DESC"

    # =========================
    # Basic fields
    # =========================

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    property_ids = fields.One2many("estate.property", "type_id", string="Properties")
   