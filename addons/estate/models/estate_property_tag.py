from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"
    _order = "name DESC"

    name = fields.Char(string="Tag Name", required=True)
    color = fields.Integer()
    _sql_constraints = [
        ('check_name', 'UNIQUE(name)', 'The tag name must be unique'),
    ]