# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Calculate withholding tax base',
    'category': 'Invoicing Management',
    'version': '12.0.0.1',
    'summary': 'Calculate withholding tax base',
    'author': 'Soluciones Softhard, C.A.',
    'website': 'http://www.solucionesofthard.com',
    # ~ 'price': 220,
    # ~ 'currency': 'EUR',
    'description': """
        Calculate withholding tax base
    """,
    'depends': ['account'],
    'data': [
        'views/account_view.xml',
    ],
    'license': "OPL-1",
    'installable': True,
    'auto_install': False,
    'application': False,
}
