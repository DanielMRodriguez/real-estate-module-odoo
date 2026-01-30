from odoo import api, fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _order = "id DESC"

    # =========================
    # Basic fields
    # =========================

    name = fields.Char(string="Title", required=True)
    description = fields.Text()

    postcode = fields.Char()
    date_availability = fields.Date(copy=False,
    default=lambda self: fields.Date.add(fields.Date.today(), months=3))

    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True,copy=False)


    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()

    garage = fields.Boolean()
    garden = fields.Boolean(default=True)

    garden_area = fields.Integer(default=10)
    garden_orientation = fields.Selection(
        [
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        default="north"
    )

    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ],
        required=True,
        copy=False,
        default='new',
    )

    type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        ondelete="restrict"
    )

    user_id = fields.Many2one('res.users', string="Salesperson",tracking=True,index=True,default=lambda self: self.env.user)
    buyer_id = fields.Many2one('res.partner',copy=False, string="Buyer",tracking=True,index=True)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    total_area = fields.Integer(compute="_compute_total_area",store=True)

    best_price = fields.Float(compute="_compute_best_price",store=True)

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = (record.living_area or 0) + (record.garden_area or 0)

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            prices = record.offer_ids.mapped('price')
            record.best_price = max(prices) if prices else 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = False

    # Cuando se haga una oferta, se debe poner el estado de la propiedad a offer_received, pero si esta como offer_accepted, offer_received o sold, no se debe cambiar el estado
    @api.onchange('offer_ids')
    def _onchange_offer_ids(self):
        for property in self:
            if property.state in ['offer_accepted', 'sold']:
                return {'warning': {'title': 'Offer received', 'message': 'The property is already in an offer state'}}
            property.state = 'offer_received'

    def cancel_sale_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("You cannot cancel a sold property")
            property.state = 'canceled'
        return True

    def confirm_sale_property(self):
        for property in self:
            if property.state == 'sold':
                raise UserError("You cannot confirm a sold property")
            offer_is_accepted = False
            offer_accepted = None
            for offer in property.offer_ids:
                if offer.status == 'accepted':
                    offer_is_accepted = True
                    offer_accepted = offer
                    break
            if not offer_is_accepted:
                raise UserError("You cannot confirm a property without an accepted offer")
            property.state = 'sold'
            property.selling_price = offer_accepted.price
            property.buyer_id = offer_accepted.partner_id 
        return True
    
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be greater than 0'),
        ('check_selling_price', 'CHECK(selling_price > 0)', 'The selling price must be greater than 0'),
    ]

    @api.ondelete(at_uninstall=True)
    def _unlink_if_not_canceled_or_new(self):
        for property in self:
            if property.state not in ['canceled', 'new']:
                raise UserError("You cannot delete a property that is not canceled or new")