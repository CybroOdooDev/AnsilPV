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
{
    'name': "Email Cc Bcc",
    'version': '16.0.1.0.0   ',
    'depends': ['base', 'mail'],
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': 'https://www.cybrosys.com',
    'category': 'Discuss',
    'description': "send mails using Cc and Bcc",
    'summary': 'Geolocation In website. '
               'This helps the users to add Cc and Bcc mails and send them separately based on Cc Bcc conditions.',
    # data files always loaded at installation

    'assets': {
        'web.assets_backend': [
            '/email_cc_bcc/static/src/xml/mail_thread_mails.xml',
        ],
        'mail.assets_messaging': [
            '/email_cc_bcc/static/src/js/mail_thread_mail.js',
        ]
    },

    'data': [
        'view/email_cc_bcc.xml',
        'view/email_compose.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}
