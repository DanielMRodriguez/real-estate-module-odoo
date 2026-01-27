from odoo import api,fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"

    price = fields.Float(string="Price",required=True,tracking=True)
    status = fields.Selection(
        string="Status",
        selection=[
            ("draft", "Draft"),
            ("accepted", "Accepted"),
            ("refused", "Refused"),
            ("canceled", "Canceled")
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
            
    def accept_offer(self):
        for offer in self:
            if offer.status != "draft":
                raise UserError("You can only accept draft offers")
            # valida que estate.property no este en estado sold
            if offer.property_id.state == "sold":
                raise UserError("You cannot accept an offer for a sold property")
            # Actualiza el estado de la oferta a accepted
            offer.status = "accepted"
            # Actualiza el estado de la propiedad a offer_accepted
            offer.property_id.state = "offer_accepted"
        return True

    def reject_offer(self):
        for offer in self:
            if offer.status != "draft":
                raise UserError("You can only reject draft offers")
            # valida que estate.property no este en estado sold
            if offer.property_id.state == "sold":
                raise UserError("You cannot reject an offer for a sold property")
            # Actualiza el estado de la oferta a refused
            offer.status = "refused"
        return True

    def cancel_offer(self):
        for offer in self:
            if offer.status != "accepted":
                raise UserError("You can only cancel accepted offers")
            # Actualiza el estado de la oferta a draft
            offer.status = "canceled"
        return True