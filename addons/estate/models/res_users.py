from odoo import api, fields, models

class ResUsers(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "user_id", string="Properties")

    available_property_ids = fields.One2many(
        "estate.property",
        "user_id",
        string="Available Properties",
        domain=[("state", "not in", ("sold", "canceled"))],
    )