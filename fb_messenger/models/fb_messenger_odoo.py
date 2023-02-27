# -*- coding: utf-8 -*-
################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Ansil pv (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#####################################################################################


from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """
    Inheriting fields into settings
    """
    _inherit = 'res.config.settings'

    enable_messenger = fields.Boolean("Enable Messenger", help="Enable for show page id field")
    fb_id_page = fields.Char("Facebook Page Id", help="To add facebook page id")

    def set_values(self):
        """
        Settings set values
        """
        res = super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('fb_messenger.enable_messenger', self.enable_messenger)
        self.env['ir.config_parameter'].set_param('fb_messenger.fb_id_page', self.fb_id_page)
        return res

    @api.model
    def get_values(self):
        """
        Settings get values
        """
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            enable_messenger=params.get_param('fb_messenger.enable_messenger'),
            fb_id_page=params.get_param('fb_messenger.fb_id_page'),
        )
        return res

    @api.onchange('fb_id_page', 'enable_messenger')
    def compute_fb_id_page(self):
        """Function for set page id to field in website that inherited from same field in settings

        """
        fb_id_page = self.fb_id_page
        website = self.env['website'].sudo().search([])
        for rec in website:
            rec.fb_id_page = fb_id_page
            if self.enable_messenger:
                rec.enable_messenger = True
            else:
                rec.enable_messenger = False


class Website(models.Model):
    """
    Inheriting fields into website
    """
    _inherit = "website"

    enable_messenger = fields.Boolean("Enable Messenger")
    fb_id_page = fields.Char("Facebook Page Id")
