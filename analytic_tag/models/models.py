# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stockmove(models.Model):
    _inherit = "stock.move"

    # analytic_tag_ids = fields.Many2one(string='Analytic Tags', comodel_name='account.analytic.tag',
    #                                    domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string='Analytic Tags')

    @api.model
    def create(self,values):
        res = super(stockmove,self).create(values)
        if res:
            if res.sale_line_id:
                if len(res.sale_line_id.analytic_tag_ids.ids) > 0:
                    res.analytic_tag_ids = [(6,0,res.sale_line_id.analytic_tag_ids.ids)]
        return res


