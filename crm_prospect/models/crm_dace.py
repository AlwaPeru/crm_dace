# -*- coding: utf-8 -*-
# Copyright (C) 2018 Juan D. Salcedo Salazar <salcedo.salazar@gmail.com>

from odoo import api, fields, models
from odoo.tools.translate import _
from odoo.exceptions import UserError


class Dace(models.Model):
    _name = "res.dace"
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True,
                                 string='Related Partner', help='Partner-related data of the user')
    supervisor_ids = fields.One2many('res.users', 'dace_id', string='Supervisor')
    num_ffvv = fields.Char(string='Nro. FFVV')
    state = fields.Selection([('active', 'Activo'),
                              ('inactive', 'Inactivo'),
                              ('interested', 'Interesado'),
                              ('not_interested', 'No Interesado'),
                              ('contacted', 'Contactado'),
                              ('not_contacted', 'No Contactado')], string='State')
    note = fields.Text(string='Notes')
    owner_id = fields.Many2one('res.users', string='Owner')
    owner_mobile = fields.Char(related='owner_id.partner_id.mobile', string='Phone')
    owner_email = fields.Char(related='owner_id.partner_id.email', string='Email')
    coordinator_claro_id = fields.Many2one('res.users', string="Claro Coordinator")

    @api.multi
    def write(self, values):
        users_obj = self.env['res.users']
        create_list = []
        if 'supervisor_ids' in values and values.get('supervisor_ids'):
            for data in values.get('supervisor_ids'):
                op = data[0] if len(data) else -1
                if op == 1:
                    if 'parent_user_id' in data[2]:
                        # Si no se tiene un 'parent_user_id'
                        if data[2].get('parent_user_id') is False:
                            user = users_obj.browse([data[1]])
                            raise UserError(_("The user: %s, should have a parent, he could be the owner or"
                                              " coordinator of the current Dace") % user.name)
                        else:
                            # El 'parent_user_id' debe ser un entity = 'claro' y si es 'dace' debe tener el mismo
                            # 'dace_id'
                            user = users_obj.browse([data[1]])
                            parent = users_obj.browse([data[2].get('parent_user_id')])
                            if parent.entity == 'dace' and parent.dace_id.id != self.id:
                                raise UserError(_("The user: %s, should have a parent from 'Claro' or the same 'Dace'")
                                                % user.name)
                            else:
                                if data[1] in create_list:
                                    create_list.remove(data[1])
                # elif op == 6:
                #     create_list.append(data[2][0])
                elif op == 3:
                    user = users_obj.browse([data[1]])
                    user.write({'parent_user_id': False, 'dace_id': False})

        # if len(create_list) > 0:
        #     raise UserError(_("Exist users without parents"))

        res = super(Dace, self).write(values)
        return res

    @api.model
    def create(self, values):
        user_obj = self.env['res.users']
        res = super(Dace, self).create(values)
        if 'owner_id' in values and 'coordinator_claro_id' in values:
            owner = user_obj.browse([values.get('owner_id')])
            coor = user_obj.browse([values.get('coordinator_claro_id')])
            owner.write({'parent_user_id': coor.id, 'dace_id': res.id})
        return res
