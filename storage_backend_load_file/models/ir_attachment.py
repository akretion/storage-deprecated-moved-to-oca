# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    from_storage_backend = fields.Boolean(
        default=False,
        help="Determine if this attachment comes from a storage backend",
    )
