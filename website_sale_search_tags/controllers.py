from odoo.addons.website_sale.controllers.main import WebsiteSale as controller

from odoo import http
from odoo.http import request


class WebsiteSale(controller):

    @http.route()
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        request.context = dict(request.context, search_tags=search)
        return super(WebsiteSale, self).shop(page, category, search, ppg, **post)
