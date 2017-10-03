# -*- coding: utf-8 -*-
# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models
import base64


import logging
logger = logging.getLogger(__name__)


class OdooStorageBackend(models.Model):
    _inherit = 'storage.backend'

    backend_type = fields.Selection(
        selection_add=[('odoo', 'Odoo')])

    def _odoo_store(self, name, datas, is_public=False, **kwargs):
        ir_attach_vals = {
            'name': name,
            'type': 'binary',
            'datas': datas,
        }
        attachment = self.env['ir.attachment'].create(ir_attach_vals)
        return attachment.id

    # This method is kind of useless but we can keep it to be consistent with
    # other storage backends
    def _odoo_retrieve(self, attach_id):
        """Retrive data from odoo attachments

        Data is already stored base64 encoded."""
        attach = self.env['ir.attachment'].browse(attach_id)
        # odoo use str.encode('base64') which adds \n
        return attach.datas.replace('\n','')

    def _odooget_public_url(self, attach_id):
        # TODO faire mieux
        logger.info('get_public_url')
        attach = self.env['ir.attachment'].browse(attach_id)
        url = (
            'web/binary/image?model=%(model)s'
            '&id=%(attach_id)s&field=datas'
            # comment on sait que c'est une image? a mettre ailleurs
        ) % {
            'model': attach._name,
            'attach_id': attach.id
        }
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        if not base_url.endswith('/'):
            base_url = base_url + '/'
        return base_url + url
