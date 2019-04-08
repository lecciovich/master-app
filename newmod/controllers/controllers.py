# -*- coding: utf-8 -*-
from odoo import http

# class Newmod(http.Controller):
#     @http.route('/newmod/newmod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/newmod/newmod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('newmod.listing', {
#             'root': '/newmod/newmod',
#             'objects': http.request.env['newmod.newmod'].search([]),
#         })

#     @http.route('/newmod/newmod/objects/<model("newmod.newmod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('newmod.object', {
#             'object': obj
#         })