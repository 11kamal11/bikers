from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BikeRental(models.Model):
    _name = 'bike.rental'
    _description = 'Bike Rental'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Bike Name", required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price per Day", required=True, default=10.0)
    image = fields.Binary(string="Image")
    is_available = fields.Boolean(string="Available", default=True, tracking=True)
    rental_duration = fields.Integer(string="Default Rental Duration (days)", default=1)
    rental_requests = fields.One2many('bike.rental.request', 'bike_id', string="Rental Requests")

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Price must be greater than zero.")

    def action_rent(self):
        for bike in self:
            if bike.is_available:
                bike.is_available = False
            else:
                raise ValidationError("This bike is already rented.")

    def action_return(self):
        for bike in self:
            if not bike.is_available:
                bike.is_available = True
            else:
                raise ValidationError("This bike is already available.")
