import uuid

from odoo import models, fields
from odoo import tools, _

try:
    from odoo.addons.email_template.email_template import mako_template_env
except ImportError:
    try:
        from odoo.addons.mail.mail_template import mako_template_env
    except ImportError:
        pass


class WebsiteProposalTemplate(models.Model):
    _name = "website_proposal.template"
    _description = "Proposal Template"
    name = fields.Char('Proposal Template', required=True)

    head = fields.Text('Html head')
    page_header = fields.Html('Page header')
    website_description = fields.Html('Description')
    page_footer = fields.Html('Page footer')

    res_model = fields.Char('Model', help="The database object this template will be applied to")

    def open_template(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/website_proposal/template/%d' % ids[0]
        }

    def create_proposal(self, template_id, res_id):
        if not template_id:
            return False
        if isinstance(template_id, list):
            template_id = template_id[0]

        template = self.env['website_proposal.template'].browse(template_id)

        vals = {'template_id': template_id,
                'head': template.head,
                'page_header': template.page_header,
                'website_description': template.website_description,
                'page_footer': template.page_footer,
                'res_id': res_id,
                'res_model': context.get('force_res_model') or template.res_model,
                }

        proposal_id = self.env['website_proposal.proposal'].create(vals, context)
        return proposal_id


class WebsiteProposal(models.Model):
    _name = 'website_proposal.proposal'
    _rec_name = 'id'

    # def _get_default_company(self):
    #     company_id = self.env['res.users']._get_company(context=context)
    #     if not company_id:
    #         raise UserError(_('Error!'), _('There is no default company for the current user!'))
    #     return company_id

    def _get_res_name(self, name, args):
        res = {}
        for r in self.browse(ids):
            record = self.env[r.res_model].browse(r.res_id)
            res[r.id] = record.name
        return res

    res_name = fields.Char(compute='_get_res_name', string='Name', type='char')
    access_token = fields.Char('Security Token', required=True, copy=False,default=lambda self: str(uuid.uuid4()),)
    template_id = fields.Many2one('website_proposal.template', 'Quote Template', readonly=True)
    head = fields.Text('Html head')
    page_header = fields.Text('Page header')
    website_description = fields.Html('Description')
    page_footer = fields.Text('Page footer')

    res_model = fields.Char('Model', readonly=True, help="The database object this is attached to")
    res_id = fields.Integer('Resource ID', readonly=True, help="The record id this is attached to", index=True)
    sign = fields.Binary('Singature')
    sign_date = fields.Datetime('Signing Date')
    signer = fields.Binary('Signer')
    state = fields.Selection([('draft', 'Draft'), ('rejected', 'Rejected'), ('done', 'Signed'), ],default= 'draft',)
    company_id = fields.Many2one('res.company', 'Company',default=lambda self: self.env.user.company_id.id,)
    # _defaults = {
    #     'access_token': lambda self, cr, uid, ctx={}: str(uuid.uuid4()),
    #     'company_id': _get_default_company,
    #     'state': 'draft',
    # }

    def open_proposal(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/website_proposal/%s' % (ids[0])
        }

    def edit_proposal(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/website_proposal/%s?enable_editor' % (ids[0])
        }

    def create(self, vals):
        record = self.env[vals.get('res_model')].browse(vals.get('res_id'))

        mako = mako_template_env.from_string(tools.ustr(vals.get('website_description')))
        website_description = mako.render({'record': record})
        website_description = website_description.replace('template-only-', '')

        vals['website_description'] = website_description
        new_id = super(WebsiteProposal, self).create(vals)
        return new_id


class MailMessageSubtype(models.Model):
    _inherit = 'mail.message.subtype'
    internal = fields.Boolean('Internal', help="don't publish these messages",default=False)
    # _defaults = {
    #     'internal': False
    # }
