# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CalendarEvent(models.Model):
    """ Model for Calendar Event """
    _inherit = 'calendar.event'

    @api.model
    def default_get(self, fields):
        if self.env.context.get('default_prospect_id'):
            self = self.with_context(
                default_res_model_id=self.env.ref('crm.model_crm_lead').id,
                default_res_id=self.env.context['default_prospect_id']
            )

        defaults = super(CalendarEvent, self).default_get(fields)

        # sync res_model / res_id to prospect id (aka creating meeting from lead chatter)
        if 'prospect_id' not in defaults and defaults.get('res_id') and (defaults.get('res_model') or defaults.get('res_model_id')):
            if (defaults.get('res_model') and defaults['res_model'] == 'crm.lead') or (defaults.get('res_model_id') and self.env['ir.model'].sudo().browse(defaults['res_model_id']).model == 'crm.lead'):
                defaults['prospect_id'] = defaults['res_id']

        return defaults

    def _compute_is_highlighted(self):
        super(CalendarEvent, self)._compute_is_highlighted()
        prospect_id = self.env.context.get('active_id')
        if self.env.context.get('active_model') == 'crm.lead' and prospect_id:
            for event in self:
                if event.prospect_id.id == prospect_id:
                    event.is_highlighted = True

    prospect_id = fields.Many2one('crm.lead', string="Prospect")