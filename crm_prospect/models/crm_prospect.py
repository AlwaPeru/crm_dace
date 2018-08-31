# -*- coding: utf-8 -*-
# Copyright (C) 2018 Juan D. Salcedo Salazar <salcedo.salazar@gmail.com>

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError, AccessError


class Lead(models.Model):
    _inherit = 'crm.lead'

    product_id = fields.Many2one('product.product', string='Product', ondelete='restrict', index=True)
    service_id = fields.Many2one('crm.product.service', string='Service')
    quantity = fields.Integer(string='Quantity')
    principal_contact = fields.Many2one('res.partner', string="Principal contact")
    dace_id = fields.Many2one('res.dace', string='Dace')
    code = fields.Char(string='Code', copy=False, readonly=True, index=True, default=lambda self: _('New'))
    prospect_meeting_count = fields.Integer('# Meetings', compute='_compute_prospect_meeting_count')

    @api.multi
    def _compute_prospect_meeting_count(self):
        meeting_data = self.env['calendar.event'].read_group([('prospect_id', 'in', self.ids)], ['prospect_id'],
                                                             ['prospect_id'])
        mapped_data = {m['prospect_id'][0]: m['prospect_id_count'] for m in meeting_data}
        for lead in self:
            lead.meeting_count = mapped_data.get(lead.id, 0)

    @api.multi
    def action_schedule_prospect_meeting(self):
        """ Open meeting's calendar view to schedule meeting on current prospect.
            :return dict: dictionary value for created Meeting view
        """
        self.ensure_one()
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        partner_ids = self.env.user.partner_id.ids
        if self.partner_id:
            partner_ids.append(self.partner_id.id)
        action['context'] = {
            'default_prospect_id': self.id,
            'default_partner_id': self.partner_id.id,
            'default_partner_ids': partner_ids,
            'default_team_id': self.team_id.id,
            'default_name': self.name,
        }
        return action

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        super(Lead, self)._onchange_partner_id()
        self.principal_contact = False

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id.services_id:
            return {
                'domain': {'service_id': [('id', 'in', self.product_id.services_id.ids)]}
            }

    @api.model
    def create(self, vals):
        if vals.get('code', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['code'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code(
                    'crm.prospect.seq') or _('New')
            else:
                vals['code'] = self.env['ir.sequence'].next_by_code('crm.prospect.seq') or _('New')
        result = super(Lead, self).create(vals)
        return result


class Service(models.Model):
    _name = 'crm.product.service'

    name = fields.Char(string='Service')


#----------------------------------------------------------
# Products
#----------------------------------------------------------
class ProductTemplate(models.Model):
    _inherit = "product.template"

    services_id = fields.Many2many('crm.product.service', 'product_service_rel', 'prod_id', 'service_id',
                                   string='Service Available')
