# -*- coding: utf-8 -*-

from odoo import models, fields, api


class stockmove(models.Model):
    _inherit = "stock.move"

    analytic_tag_ids = fields.Many2many('account.analytic.tag',store = True)



    @api.model
    def create(self,values):
        res = super(stockmove,self).create(values)
        if res:
            if res.sale_line_id:
                if len(res.sale_line_id.analytic_tag_ids.ids) > 0:
                    res.analytic_tag_ids = [(6,0,res.sale_line_id.analytic_tag_ids.ids)]
        return res



    def _prepare_account_move_line(
            self, qty, cost, credit_account_id, debit_account_id,description):
        result = super()._prepare_account_move_line(
            qty=qty, cost=cost, credit_account_id=credit_account_id,
            debit_account_id=debit_account_id, description=description)
        for res in result:
            res[2]['analytic_tag_ids'] = [(6, 0, self.analytic_tag_ids.ids)]
        return result






class AccountMoveLine(models.Model):

    _inherit = "account.move.line"

    analytic_distribution_ids = fields.Many2many(
        'account.analytic.distribution',
        'account_move_line_analytic_distrib_rel',
        'move_line_id',
        'analytic_distribution_id',
        string='Analytic Distribution')


    @api.constrains("analytic_distribution_ids")
    def _check_unique_analytic_account_per_move_line(self):
        analytic_accounts = []
        for account_analytic_distrib in self.analytic_distribution_ids:
            aa_id = account_analytic_distrib.analytic_account_id.id
            analytic_accounts.append(aa_id)


    def create_analytic_lines(self):
        """
        Create analytic items upon validation of an account.move.line having an
        analytic account. This method first remove any existing analytic item
        related to the line before creating any new one.
        """
        for obj_line in self:
            if obj_line.analytic_distribution_ids:
                if obj_line.analytic_line_ids:
                    obj_line.analytic_line_ids.unlink()
                vals_line_list = obj_line._prepare_analytic_lines()[0]
                for vals_line in vals_line_list:
                    self.env['account.analytic.line'].create(vals_line)


    def _prepare_analytic_lines(self):
        """
        Prepare the values used to create() an account.analytic.line upon
        validation of an account.move.line having an analytic account.
        This method is intended to be extended in other modules.
        """
        vals_list = []
        for distribution in self.analytic_distribution_ids:
            vals_list.append({
                'name': self.name,
                'date': self.date,
                'account_id': distribution.analytic_account_id.id,
                'tag_id': distribution.analytic_tag_ids.ids,
                'unit_amount': self.quantity,
                'product_id': self.product_id and self.product_id.id or False,
                'product_uom_id': self.product_uom_id and self.product_uom_id.id or False,
                'amount': ((self.credit or 0.0) - (self.debit or 0.0)) * distribution.rate / 100,
                'general_account_id': self.account_id.id,
                'ref': self.ref,
                'move_id': self.id,
                'user_id': self.invoice_id.user_id.id or self._uid,
            })
        return vals_list

    @api.constrains("analytic_distribution_ids")
    def check_analytic_distribution_ids(self):
        AccountAnalyticAxis = self.env['account.analytic.axis']
        return AccountAnalyticAxis.check_percent_on_axis(
            self.analytic_distribution_ids)
