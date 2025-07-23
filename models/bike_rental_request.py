from odoo import models, fields, api
from odoo.exceptions import ValidationError

class BikeRentalRequest(models.Model):
    _name = 'bike.rental.request'
    _description = 'Bike Rental Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'

    name = fields.Char(string="Customer Name", required=True)
    bike_id = fields.Many2one('bike.rental', string="Bike", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    duration = fields.Integer(string="Duration (days)", required=True)
    user_id = fields.Many2one('res.users', string="Requested By", default=lambda self: self.env.user)
    request_date = fields.Date(string="Request Date", default=fields.Date.today)
    state = fields.Selection([
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Status", default='pending', tracking=True)

    @api.constrains('duration')
    def _check_duration(self):
        for request in self:
            if request.duration <= 0:
                raise ValidationError("Duration must be greater than zero.")

    @api.constrains('start_date')
    def _check_start_date(self):
        for request in self:
            if request.start_date < fields.Date.today():
                raise ValidationError("Start date cannot be in the past.")

    def action_approve(self):
        for request in self:
            if request.state == 'pending':
                request.bike_id.action_rent()
                request.state = 'approved'
            else:
                raise ValidationError("Only pending requests can be approved.")

    def action_reject(self):
        for request in self:
            if request.state == 'pending':
                request.state = 'rejected'
            else:
                raise ValidationError("Only pending requests can be rejected.")
