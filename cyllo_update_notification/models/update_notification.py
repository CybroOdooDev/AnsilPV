# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CylloUpdateNotification(models.Model):
    """One row per publisher-warranty ping received from an Odoo instance.

    The sender is `publisher_warranty.contract._get_sys_logs()` in
    addons/mail/models/update.py, driven by the weekly
    `mail.ir_cron_module_update_notification` cron. Every field below maps a
    key of the dict that method builds in `_get_message()`.
    """
    _name = 'cyllo.update.notification'
    _description = 'Received Update Notification'
    _order = 'received_date desc, id desc'
    _rec_name = 'dbname'

    received_date = fields.Datetime(
        string='Received On', required=True, readonly=True, index=True,
        default=fields.Datetime.now)
    remote_addr = fields.Char(string='Source IP', readonly=True)

    # --- identity ---------------------------------------------------------
    dbuuid = fields.Char(string='Database UUID', readonly=True, index=True)
    dbname = fields.Char(string='Database Name', readonly=True, index=True)
    db_create_date = fields.Char(
        string='Database Created', readonly=True,
        help="Sent as the raw `database.create_date` config parameter, so it "
             "is kept as text rather than parsed into a Datetime.")
    version = fields.Char(string='Odoo Version', readonly=True)
    language = fields.Char(string='User Language', readonly=True)
    web_base_url = fields.Char(string='Web Base URL', readonly=True)
    enterprise_code = fields.Char(string='Enterprise Code', readonly=True)

    # --- usage ------------------------------------------------------------
    nbr_users = fields.Integer(string='Users', readonly=True)
    nbr_active_users = fields.Integer(
        string='Active Users', readonly=True,
        help="Users who logged in within the 15 days before the ping.")
    nbr_share_users = fields.Integer(string='Portal Users', readonly=True)
    nbr_active_share_users = fields.Integer(
        string='Active Portal Users', readonly=True)
    apps = fields.Text(
        string='Installed Apps', readonly=True,
        help="Names of every module flagged as an Application and installed, "
             "to upgrade or to remove on the sender.")
    app_count = fields.Integer(
        string='App Count', compute='_compute_app_count', store=True)

    # --- company ----------------------------------------------------------
    # Only sent when the acting user's partner has a company; _get_message()
    # merges company_id.read(['name', 'email', 'phone'])[0] into the payload.
    company_name = fields.Char(string='Company', readonly=True)
    company_email = fields.Char(string='Company Email', readonly=True)
    company_phone = fields.Char(string='Company Phone', readonly=True)

    raw_payload = fields.Text(
        string='Raw Payload', readonly=True,
        help="The `arg0` field exactly as received, kept so that keys a newer "
             "Odoo version might add are not lost even though there is no "
             "column for them yet.")

    @api.depends('apps')
    def _compute_app_count(self):
        for record in self:
            names = (record.apps or '').split(',')
            record.app_count = len([n for n in names if n.strip()])

    @api.model
    def _vals_from_payload(self, payload, remote_addr=None):
        """Map one decoded `arg0` dict onto this model's fields.

        Unrecognised keys are intentionally not mapped - `raw_payload` keeps
        the original so nothing is lost.

        Note the payload also carries an `id`: `_get_message()` merges
        `company_id.read([...])[0]`, and read() always returns the record id.
        That is the *company's* id on the sending database and means nothing
        here, so it is dropped on purpose rather than mistaken for a
        reference.
        """
        def as_int(key):
            try:
                return int(payload.get(key) or 0)
            except (TypeError, ValueError):
                return 0

        apps = payload.get('apps') or []
        if isinstance(apps, (list, tuple, set)):
            apps = ', '.join(str(app) for app in apps)

        return {
            'remote_addr': remote_addr,
            'dbuuid': payload.get('dbuuid'),
            'dbname': payload.get('dbname'),
            'db_create_date': payload.get('db_create_date'),
            'version': payload.get('version'),
            'language': payload.get('language'),
            'web_base_url': payload.get('web_base_url'),
            'enterprise_code': payload.get('enterprise_code'),
            'nbr_users': as_int('nbr_users'),
            'nbr_active_users': as_int('nbr_active_users'),
            'nbr_share_users': as_int('nbr_share_users'),
            'nbr_active_share_users': as_int('nbr_active_share_users'),
            'apps': apps,
            # `name` / `email` / `phone` are the sender company's, not this
            # record's - see the docstring above.
            'company_name': payload.get('name'),
            'company_email': payload.get('email'),
            'company_phone': payload.get('phone'),
        }
