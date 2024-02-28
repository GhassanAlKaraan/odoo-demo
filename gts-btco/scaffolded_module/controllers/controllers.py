# -*- coding: utf-8 -*-
# from odoo import http


# class ScaffoldedModule(http.Controller):
#     @http.route('/scaffolded_module/scaffolded_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/scaffolded_module/scaffolded_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('scaffolded_module.listing', {
#             'root': '/scaffolded_module/scaffolded_module',
#             'objects': http.request.env['scaffolded_module.scaffolded_module'].search([]),
#         })

#     @http.route('/scaffolded_module/scaffolded_module/objects/<model("scaffolded_module.scaffolded_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('scaffolded_module.object', {
#             'object': obj
#         })

