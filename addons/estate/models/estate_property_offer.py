from odoo import api,fields, models
from odoo.tools import float_compare
from datetime import date, timedelta
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price DESC"

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
            ##si la propiedad no tiene otras ofertas que no esten canceladas, se debe poner en new, si tiene otras ofertas, se debe poner en offer_received
            if len(offer.property_id.offer_ids.filtered(lambda o: o.status != "canceled")) == 0:
                offer.property_id.state = "new"
            else:
                offer.property_id.state = "offer_received"   
        return True

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            # selling prices cannot be lower than 90% of the expected price, use float_compare from odoo.tools
            if not float_compare(record.price, record.property_id.expected_price * 0.9, precision_digits=2) >= 0:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price")
            if record.price <= 0:
                raise ValidationError("The price must be greater than 0")