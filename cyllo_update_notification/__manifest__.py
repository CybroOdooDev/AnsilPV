# -*- coding: utf-8 -*-
{
    'name': 'Cyllo Update Notification Receiver',
    'version': '17.0.1.0.0',
    'category': 'Technical',
    'summary': "Receive and store the publisher-warranty pings Odoo instances "
               "send on their weekly update-notification cron",
    'description': """
Cyllo Update Notification Receiver
==================================
Stands in for Odoo's own publisher-warranty service.

`publisher_warranty.contract._get_sys_logs()` (addons/mail/models/update.py)
POSTs a weekly ping to whatever `publisher_warranty_url` points at, carrying
the sending database's uuid and name, its Odoo version, user counts, installed
apps, web base URL and — when the acting user's partner has one — the
company's name, email and phone.

Pointing `publisher_warranty_url` at this module's `/publisher-warranty`
endpoint keeps that data in-house: every ping is stored as one
`cyllo.update.notification` record, viewable under
Settings > Technical > Update Notifications.

The reply is deliberately minimal — `{'messages': []}`. It carries no
`enterprise_info`, so this endpoint can never rewrite a sender's
`database.expiration_date` or subscription parameters.

Nothing in `mail` is patched: the sender already reads its target from the
configuration, so only `publisher_warranty_url` has to change.
""",
    'author': 'Cybrosys Technologies',
    'company': 'Cybrosys Technologies',
    'maintainer': 'Cybrosys Technologies',
    'website': 'https://www.cybrosys.com',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/update_notification_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
