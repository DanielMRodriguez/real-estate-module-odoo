from odoo import api,fields, models
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(string="Price",required=True,tracking=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        default="draft"
    )

    partner_id = fields.Many2one('res.partner', string="Partner",tracking=True,index=True)
    property_id = fields.Many2one('estate.property', string="Property",tracking=True,index=True)

    validity = fields.Integer(string="Validity (days)",default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.context_today(record)
            record.date_deadline = start_date + timedelta(days=record.validity or 0)
    

    def _inverse_date_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.context_today(record)
            if record.date_deadline:
                record.validity = (record.date_deadline - start_date).days
            else:
                record.validity = 0
            
