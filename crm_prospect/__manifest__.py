{
    'name': 'Prospecto',
    'version': '1.0',
    'summary': 'Permite registrar Prospectos',
    'sequence': 40,
    'description': """
        Módulo permite a los vendedores de Claro Empresas registrar prospectos.
    """,
    'author': "Salcedo Salazar Juan Diego",
    'website': 'http://alwaperu.pe/',
    'depends': [
        'base',
        'crm',
        'odoope_toponyms',
        'product',
    ],
    'data': [
        'security/crm_prospect_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/crm_kpi_view.xml',
        'views/res_partner_view.xml',
        'views/res_users_views.xml',
        'views/crm_prospect_views.xml',
        'views/product_view.xml',
        'views/service_view.xml',
        'views/crm_dace_view.xml',
        'views/crm_mobility_view.xml',
        'views/crm_prospect_menu.xml',
    ],
    'demo': [
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
}
# -*- coding: utf-8 -*-
# Copyright (C) 2018 Juan D. Salcedo Salazar <salcedo.salazar@gmail.com>
