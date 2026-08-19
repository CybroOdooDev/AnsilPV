# -*- coding: utf-8 -*-

import ast
import logging

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

# `arg0` is a repr()'d dict of counters and short strings; even a few hundred
# installed apps is only a handful of KB. Anything past this is not a genuine
# ping, and handing literal_eval an unbounded string from an unauthenticated
# caller is not worth doing.
MAX_PAYLOAD_BYTES = 64 * 1024

# What services.odoo.com answers with, reduced to the minimum.
#
# `messages` is not optional: update_notification() reads result["messages"]
# with no guard (addons/mail/models/update.py), so leaving it out turns every
# ping into a failing cron on the sender.
#
# `enterprise_info` is deliberately absent. When present, the sender writes
# database.expiration_date / expiration_reason / enterprise_code and the
# already-linked-subscription parameters straight from it - so replying with it
# would let this endpoint change subscription state on every instance that
# points here.
#
# It is also a *Python literal*, not JSON: the sender parses the body with
# ast.literal_eval, not json.loads.
REPLY_BODY = "{'messages': []}"


class PublisherWarrantyReceiver(http.Controller):
    """Local stand-in for Odoo's publisher-warranty service."""

    @http.route(['/publisher-warranty', '/publisher-warranty/'],
                type='http', auth='public', methods=['POST'],
                csrf=False, save_session=False)
    def publisher_warranty(self, **post):
        """Store one publisher-warranty ping and acknowledge it.

        The sender POSTs form-encoded `action=update` plus
        `arg0=<repr of a dict>`, calls `raise_for_status()` and then
        literal_eval()s the body - so this has to answer 200 with a Python
        literal.

        `save_session=False` keeps a weekly ping from every instance out of
        the session store; `auth='public'` because the caller has no session
        at all.
        """
        try:
            self._store_ping(post)
        except Exception:
            # Never let a storage problem reach the sender. Its cron calls
            # update_notification(None) - cron_mode is falsy, so exceptions
            # there are *not* swallowed and a 500 here would surface as a
            # failed "Publisher: Update Notification" scheduled action on a
            # database we do not control.
            _logger.exception("publisher-warranty: failed to store ping")
        return request.make_response(
            REPLY_BODY,
            headers=[('Content-Type', 'text/plain; charset=utf-8')],
        )

    def _store_ping(self, post):
        """Validate `post` and create one record. Silently ignores junk."""
        action = post.get('action')
        if action != 'update':
            _logger.info("publisher-warranty: ignoring action=%r", action)
            return

        raw = post.get('arg0') or ''
        if not raw:
            _logger.warning("publisher-warranty: ping carried no arg0")
            return
        if len(raw) > MAX_PAYLOAD_BYTES:
            _logger.warning(
                "publisher-warranty: rejected arg0 of %d bytes (limit %d)",
                len(raw), MAX_PAYLOAD_BYTES)
            return

        try:
            payload = ast.literal_eval(raw)
        except (ValueError, SyntaxError, TypeError, MemoryError, RecursionError):
            _logger.warning("publisher-warranty: arg0 is not a Python literal")
            return

        if not isinstance(payload, dict):
            _logger.warning(
                "publisher-warranty: arg0 decoded to %s, expected dict",
                type(payload).__name__)
            return

        Notification = request.env['cyllo.update.notification'].sudo()
        vals = Notification._vals_from_payload(
            payload, request.httprequest.remote_addr)
        vals['raw_payload'] = raw
        record = Notification.create(vals)
        _logger.info(
            "publisher-warranty: stored ping %s from db %r (uuid %s, %s users)",
            record.id, record.dbname, record.dbuuid, record.nbr_users)
