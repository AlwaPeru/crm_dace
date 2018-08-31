# -*- coding: utf-8 -*-
# Copyright (C) 2018 Juan D. Salcedo Salazar <salcedo.salazar@gmail.com>

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import ValidationError


class JobTitle(models.Model):
    _name = 'res.job.title'
    _order = 'name'

    name = fields.Char(string='Title', required=True, translate=True)
    shortcut = fields.Char(string='Abbreviation', translate=True)


class Users(models.Model):
    _inherit = 'res.users'

    _parent_name = "parent_user_id"
    _parent_store = True
    _parent_order = 'name2'
    _order = 'parent_left'

    name2 = fields.Char(related='partner_id.name', store=True)
    complete_name = fields.Char(string='Complete Name', compute='_compute_complete_name', store=True)
    dace_id = fields.Many2one('res.dace', string='Dace Assignation')
    parent_user_id = fields.Many2one('res.users', string='Parent', index=True)
    child_user_ids = fields.One2many('res.users', 'parent_user_id', string='Childs')
    parent_left = fields.Integer('Left Parent', index=True)
    parent_right = fields.Integer('Right Parent', index=True)
    job_title = fields.Many2one('res.job.title', string='Job Title')
    entity = fields.Selection([('claro', 'Claro'), ('dace', 'Dace')], string='Entity')

    @api.constrains('parent_user_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('Error ! You cannot create recursive Users.'))

    @api.depends('name', 'parent_user_id.complete_name')
    def _compute_complete_name(self):
        for user in self:
            if user.parent_user_id:
                user.complete_name = '%s / %s' % (user.parent_user_id.complete_name, user.name)
            else:
                user.complete_name = user.name
