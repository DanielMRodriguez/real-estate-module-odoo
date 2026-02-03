from odoo import api, fields, models, Command
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class EstateProperty(models.Model):
    _inherit = "estate.property"

    _logger = logging.getLogger(__name__)
    def confirm_sale_property(self):
        res=super(EstateProperty, self).confirm_sale_property()
        for property in self:
            if property.state != 'sold':
                continue

            if not property.buyer_id:
                raise UserError("Buyer is required to confirm sale")

            journal = self.env['account.journal'].search([
                ('type', '=', 'sale'),
                ('company_id', '=', property.company_id.id if hasattr(property, 'company_id') else self.env.company.id),
            ],limit=1)

            if not journal:
                raise UserError("Sales journal not found")
            
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': self.buyer_id.id,
                'journal_id': journal.id,
                'name': f"Sale of {self.name} - {self.postcode}",
                'line_ids': [
                    Command.create({
                        'name': f"Sale of {self.name} - {self.postcode}",
                        'quantity': 1,
                        'price_unit': self.selling_price,
                    }),
                    Command.create({
                        'name': "Administrative fees",
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                    Command.create({
                        'name': 'Commission (6%)',
                        'quantity': 1,
                        'price_unit': self.selling_price * 0.06,
                    })
                ]
            })
        
        return res