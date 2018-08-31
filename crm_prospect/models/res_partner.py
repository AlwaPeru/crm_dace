# -*- coding: utf-8 -*-
# Copyright (C) 2018 Juan D. Salcedo Salazar <salcedo.salazar@gmail.com>

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = 'res.partner'

    tradename = fields.Char(string='Tradename')
    business_type = fields.Selection([('mype', 'Mype'),
                                      ('mid_emp', 'Mediana Empresa'),
                                      ('gran_emp', 'Gran Empresa'),
                                      ('corp', 'Corporaciones')], string='Business Type')
    legal_rep = fields.Char(string='Legal Representative')
    reference = fields.Char(string='Reference')
    work_item = fields.Selection([('banking', 'Banca'),
                                  ('agro', 'Agrícola'),
                                  ('comerce', 'Comercio')], string='Work Item')
    zone_type = fields.Selection([('urb', 'Urbanización'), ('fundo', 'Fundo'), ('none', '-'),
                                  ('publo_joven', 'Pueblo Joven'), ('aso_prov_viv', 'Asoc. Pro Vivienda'),
                                  ('unid_vec', 'Unidad Vecinal'), ('con_hab', 'Conjunto Habitacional'),
                                  ('asent_hum', 'Asentamiento Humano'), ('sector', 'Sector'), ('coop', 'Cooperativa'),
                                  ('comunid_campes', 'Comunid. Campesina'), ('comunidad', 'Comunidad'),
                                  ('resid', 'Recidencial'), ('zona_ind', 'Zona Industrial'),
                                  ('centro_pob', 'Centro Poblado'), ('grupo', 'Grupo'), ('condo', 'Condominio'),
                                  ('caserio', 'Caserío'), ('hacienda', 'Hacienda'), ('villa', 'Villa'),
                                  ('anexo', 'Anexo'), ('otros', 'Otros')
                                  ], string='Zone type')
    zone_name = fields.Char(string='Zone name')
    via_type = fields.Selection([('av', 'Avenida'), ('boulrd', 'Boulevard'), ('camino', 'Camino'),
                                 ('jiron', 'Jiron'), ('calle', 'Calle'), ('pasaje', 'Pasaje'),
                                 ('alameda', 'Alameda'), ('malecon', 'Malecón'), ('ovalo', 'Óvalo'),
                                 ('parque', 'Parque'), ('plaza', 'Plaza'), ('carr', 'Carretera'), ('bloc', 'Block'),
                                 ('none', '-'), ('galeria', 'Galería'), ('prolong', 'Prolongación'), ('paseo', 'Paseo')
                                 ], string='Via type')
    via_name = fields.Char(string='Via name')
    num_type = fields.Selection([('num', 'Número'), ('km', 'Kilómetro'), ('mz_lote', 'Manzana/Lote'),
                                 ('dep', 'Departamento'), ('int', 'Interior')], string='Num. type')
    number = fields.Char(string='Number')
    street_ref = fields.Text(string='Street Ref.')

    sivco_date_assignment = fields.Date('Date assignment')
    sivco_date_release = fields.Date('Date Release')
    sivco_state = fields.Selection([('assigned', 'Asignada'),
                                    ('free', 'Libre'),
                                    ('reserved', 'Reservada')], string='State')

    principal = fields.Boolean(string='Principal')
    birthday = fields.Date('Date of Birth')
    fidelity = fields.Selection([('movistar', 'Movistar'),
                                 ('entel', 'Entel'),
                                 ('claro', 'Claro')], string='Fidelity')
    anniversary = fields.Date('Anniversary')
