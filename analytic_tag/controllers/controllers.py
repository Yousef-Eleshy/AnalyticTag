# -*- coding: utf-8 -*-
# from odoo import http


# class AnalyticTag(http.Controller):
#     @http.route('/analytic_tag/analytic_tag/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/analytic_tag/analytic_tag/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('analytic_tag.listing', {
#             'root': '/analytic_tag/analytic_tag',
#             'objects': http.request.env['analytic_tag.analytic_tag'].search([]),
#         })

#     @http.route('/analytic_tag/analytic_tag/objects/<model("analytic_tag.analytic_tag"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('analytic_tag.object', {
#             'object': obj
#         })
