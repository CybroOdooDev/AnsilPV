# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Cybrosys Techno Solutions(<https://www.cybrosys.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################


import datetime
import email
from email.message import EmailMessage
from email.utils import make_msgid
import logging
from odoo.loglevels import ustr
from odoo.tools import pycompat
from odoo import models, fields, api, tools, _

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = 'res.company'

    display_cc = fields.Boolean("Display Cc")
    display_bcc = fields.Boolean("Display Bcc")
    display_replay_to = fields.Boolean("Display Replay To")
    display_reci_cc = fields.Boolean("Display Recipients Cc")
    display_reci_bcc = fields.Boolean("Display Recipients Bcc")
    default_cc = fields.Char("Default Cc")
    default_bcc = fields.Char("Default Bcc")
    default_replay_to = fields.Char("Default Replay To")


class MailComposer(models.TransientModel):
    _inherit = "mail.compose.message"

    email_to = fields.Char("To")
    email_cc = fields.Char("Cc")
    email_bcc = fields.Char("Bcc")
    email_replay_to = fields.Char("Replay-to")
    email_cc_partner_ids = fields.Many2many('res.partner', relation='res_partner_mail_cc_rel', string="Cc(Partners)")
    email_bcc_partner_ids = fields.Many2many('res.partner', relation='res_partner_mail_bcc_rel', string="Bcc(Partners)")
    cc_partner_visibility = fields.Boolean(default=False)
    bcc_partner_visibility = fields.Boolean(default=False)
    email_cc_visible = fields.Boolean(default=False)
    email_bcc_visible = fields.Boolean(default=False)
    email_rply_to_visible = fields.Boolean(default=False)

    @api.model
    @api.onchange('partner_ids')
    def default_value(self):
        cc = self.env['res.company'].search([])
        for i in cc:
            if i.id == self.env.user.company_id.id:
                if self.template_id:
                    self.email_cc = i.default_cc
                    self.email_bcc = i.default_bcc
                    self.email_replay_to = i.default_replay_to
                if i.display_reci_cc:
                    self.cc_partner_visibility = True
                if i.display_reci_bcc:
                    self.bcc_partner_visibility = True
                if i.display_cc:
                    self.email_cc_visible = True
                if i.display_bcc:
                    self.email_bcc_visible = True
                if i.display_replay_to:
                    self.email_rply_to_visible = True


class IrMailServer(models.Model):
    _inherit = 'ir.mail_server'

    def build_email(self, email_from, email_to, subject, body, email_cc=None, email_bcc=None, reply_to=False,
                    attachments=None, message_id=None, references=None, object_id=False, subtype='plain', headers=None,
                    body_alternative=None, subtype_alternative='plain'):
        """Constructs an RFC2822 email.message.Message object based on the keyword arguments passed, and returns it.

           :param string email_from: sender email address
           :param list email_to: list of recipient addresses (to be joined with commas)
           :param string subject: email subject (no pre-encoding/quoting necessary)
           :param string body: email body, of the type ``subtype`` (by default, plaintext).
                               If html subtype is used, the message will be automatically converted
                               to plaintext and wrapped in multipart/alternative, unless an explicit
                               ``body_alternative`` version is passed.
           :param string body_alternative: optional alternative body, of the type specified in ``subtype_alternative``
           :param string reply_to: optional value of Reply-To header
           :param string object_id: optional tracking identifier, to be included in the message-id for
                                    recognizing replies. Suggested format for object-id is "res_id-model",
                                    e.g. "12345-crm.lead".
           :param string subtype: optional mime subtype for the text body (usually 'plain' or 'html'),
                                  must match the format of the ``body`` parameter. Default is 'plain',
                                  making the content part of the mail "text/plain".
           :param string subtype_alternative: optional mime subtype of ``body_alternative`` (usually 'plain'
                                              or 'html'). Default is 'plain'.
           :param list attachments: list of (filename, filecontents) pairs, where filecontents is a string
                                    containing the bytes of the attachment
           :param message_id:
           :param references:
           :param list email_cc: optional list of string values for CC header (to be joined with commas)
           :param list email_bcc: optional list of string values for BCC header (to be joined with commas)
           :param dict headers: optional map of headers to set on the outgoing mail (may override the
                                other headers, including Subject, Reply-To, Message-Id, etc.)
           :rtype: email.message.EmailMessage
           :return: the new RFC2822 email message
        """
        email_from = email_from or self._get_default_from_address()
        assert email_from, "You must either provide a sender address explicitly or configure " \
                           "using the combination of `mail.catchall.domain` and `mail.default.from` " \
                           "ICPs, in the server configuration file or with the " \
                           "--email-from startup parameter."

        headers = headers or {}  # need valid dict later
        replay_to_mail = self.env['mail.compose.message'].search([], limit=1, order='id desc').mapped('email_replay_to')
        email_cc = self.env['mail.compose.message'].search([], limit=1, order='id desc').mapped('email_cc')
        email_bcc = self.env['mail.compose.message'].search([], limit=1, order='id desc').mapped('email_bcc')
        body = body or u''
        msg = EmailMessage(policy=email.policy.SMTP)
        msg.set_charset('utf-8')

        if not message_id:
            if object_id:
                message_id = tools.generate_tracking_message_id(object_id)
            else:
                message_id = make_msgid()
        msg['Message-Id'] = message_id
        if references:
            msg['references'] = references
        msg['Subject'] = subject
        msg['From'] = email_from
        del msg['Reply-To']
        if replay_to_mail:
            msg['Reply-To'] = replay_to_mail
        else:
            msg['Reply-To'] = reply_to or email_from
        msg['To'] = email_to
        if email_cc:
            msg['Cc'] = email_cc
        if email_bcc:
            msg['Bcc'] = email_bcc
        msg['Date'] = datetime.datetime.utcnow()
        for key, value in headers.items():
            msg[pycompat.to_text(ustr(key))] = value

        email_body = ustr(body)
        if subtype == 'html' and not body_alternative:
            msg.add_alternative(tools.html2plaintext(email_body), subtype='plain', charset='utf-8')
            msg.add_alternative(email_body, subtype=subtype, charset='utf-8')
        elif body_alternative:
            msg.add_alternative(ustr(body_alternative), subtype=subtype_alternative, charset='utf-8')
            msg.add_alternative(email_body, subtype=subtype, charset='utf-8')
        else:
            msg.set_content(email_body, subtype=subtype, charset='utf-8')

        if attachments:
            for (fname, fcontent, mime) in attachments:
                maintype, subtype = mime.split('/') if mime and '/' in mime else ('application', 'octet-stream')
                msg.add_attachment(fcontent, maintype, subtype, filename=fname)
        return msg
