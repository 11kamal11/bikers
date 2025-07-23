from odoo import http
from odoo.http import request
from datetime import datetime

class BikeRentalController(http.Controller):

    @http.route('/bikes', type='http', auth='public', website=True)
    def bike_list(self, **kwargs):
        """Display available bikes for rental"""
        bikes = request.env['bike.rental'].sudo().search([('is_available', '=', True)])
        success = kwargs.get('success')
        error = kwargs.get('error')
        
        return request.render('bike_rental.bike_list_template', {
            'bikes': bikes,
            'success': success,
            'error': error,
        })

    @http.route('/bikes/request', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def bike_request(self, **post):
        """Handle bike rental request submission"""
        try:
            # Validate required fields
            if not all(k in post for k in ['bike_id', 'name', 'start_date', 'duration']):
                return request.redirect('/bikes?error=Missing required fields')
            
            # Validate start date
            start_date = datetime.strptime(post['start_date'], '%Y-%m-%d').date()
            if start_date < datetime.now().date():
                return request.redirect('/bikes?error=Start date cannot be in the past')
            
            # Validate duration
            duration = int(post['duration'])
            if duration < 1:
                return request.redirect('/bikes?error=Duration must be at least 1 day')
            
            # Check if bike exists and is available
            bike = request.env['bike.rental'].sudo().browse(int(post['bike_id']))
            if not bike.exists() or not bike.is_available:
                return request.redirect('/bikes?error=Selected bike is not available')
            
            # Create rental request
            request.env['bike.rental.request'].sudo().create({
                'name': post['name'],
                'bike_id': int(post['bike_id']),
                'start_date': start_date,
                'duration': duration,
                'user_id': request.env.user.id if request.env.user.id != request.env.ref('base.public_user').id else False,
            })
            
            return request.redirect('/bikes?success=Rental request submitted successfully!')
            
        except Exception as e:
            return request.redirect('/bikes?error=An error occurred while processing your request')

    @http.route('/my/bike-requests', type='http', auth='user', website=True)
    def my_requests(self):
        """Display user's rental requests"""
        requests = request.env['bike.rental.request'].search([
            ('user_id', '=', request.env.user.id)
        ])
        
        return request.render('bike_rental.my_requests_template', {
            'requests': requests,
        })
