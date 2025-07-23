from odoo import http
from odoo.http import request

class BikeRentalController(http.Controller):
    @http.route('/bikes', type='http', auth='public', website=True)
    def bike_list(self, **kwargs):
        bikes = request.env['bike.rental'].sudo().search([('is_available', '=', True)])
        success = kwargs.get('success')
        error = kwargs.get('error')
        return request.render('bike_rental.bike_list_template', {
            'bikes': bikes,
            'success': success,
            'error': error,
        })

    @http.route('/bikes/request', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def bike_request(self, **kwargs):
        try:
            bike_id = int(kwargs.get('bike_id'))
            bike = request.env['bike.rental'].sudo().browse(bike_id)
            if not bike or not bike.is_available:
                return request.redirect('/bikes?error=Selected bike is not available.')
            
            request.env['bike.rental.request'].sudo().create({
                'name': kwargs.get('name'),
                'bike_id': bike_id,
                'start_date': kwargs.get('start_date'),
                'duration': int(kwargs.get('duration')),
                'user_id': request.env.user.id if not request.env.user == request.env.ref('base.public_user') else False,
            })
            return request.redirect('/bikes?success=Your request has been submitted.')
        except Exception as e:
            return request.redirect(f'/bikes?error={str(e)}')

    @http.route('/my/bike-requests', type='http', auth='user', website=True)
    def my_requests(self, **kwargs):
        requests = request.env['bike.rental.request'].sudo().search([('user_id', '=', request.env.user.id)])
        return request.render('bike_rental.my_requests_template', {
            'requests': requests,
        })