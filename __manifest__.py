{
    'name': 'Bike Rental',
    'version': '1.0.0',
    'category': 'Website/Website',
    'summary': 'Bike Rental Management System',
    'description': """
        A complete bike rental management system with website integration.
        Features:
        - Bike management
        - Rental requests
        - Website integration
        - User portal
    """,
    'author': 'Kamal',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'website', 'portal'],
    'data': [
        'security/models.xml',
        'security/ir.model.access.csv',
        'views/bike_rental_views.xml',
        'views/bike_rental_request_views.xml',
        'views/website_bike_rental_templates.xml',
        'data/bike_rental_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bike_rental/static/src/css/bike_rental.css',
            'bike_rental/static/src/js/bike_rental.js',
        ],
    },
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}