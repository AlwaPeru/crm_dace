# -*- coding: utf-8 -*-
# Copyright (C) 2018 Juan D. Salcedo Salazar <salcedo.salazar@gmail.com>

from odoo import api, fields, models
from odoo.tools.translate import _


class Mobility(models.Model):
    _name = 'crm.mobility'

    name = fields.Char(string='Code', copy=False, readonly=True, index=True, default=lambda self: _('New'))
    calendar_event_id = fields.Many2one('calendar.event', string='Meeting')
    district_origin_id = fields.Many2one('res.country.state', string='Origin')
    district_destiny_id = fields.Many2one('res.country.state', string='Destiny')
    date = fields.Date(string='Date')
    transport = fields.Selection([('public', 'Público'),
                                  ('private', 'Privado')], string='Transport')
    amount = fields.Float(string='Amount')
    observation = fields.Text(string='Observation')
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, track_visibility='onchange',
                              default=lambda self: self.env.user)
    dace_id = fields.Many2one('res.dace', related='user_id.dace_id', string='Dace', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'crm.mobility.seq') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('crm.mobility.seq') or _('New')
        result = super(Mobility, self).create(vals)
        return result
