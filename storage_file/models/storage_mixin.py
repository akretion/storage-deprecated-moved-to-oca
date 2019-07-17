# -*- coding: utf-8 -*-
# Copyright 2019 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class StorageFileProductMixin(models.AbstractModel):
    _name = "storage.file.product.mixin"
    _description = "Storage File Product Mixin"

    def button_product2storage(self):
        self.ensure_one()
        ctx = dict(self.env.context)
        print("\n\n", ctx)
        if self.env.context.get('active_id'):
            product_tmpl_id = self.env.context('active_id')
            ctx.update({"default_product_tmpl_id": self.env.context[
                'active_id']})
            print("\nactive_id")
        if ctx.get('params'):
            product_tmpl_id = ctx['params'].get('id')
            ctx.update({"default_product_tmpl_id": ctx['params'].get('id')})
            print("\n\nparams")
        return {
            'name': _('Files to append to product'),
            'view_mode': 'tree',
            # This key comes from storage_image_product
            # and storage_media_product modules
            'res_model': self.env.context.get('dest_model'),
            'type': 'ir.actions.act_window',
            'context': {'default_product_tmpl_id': product_tmpl_id},
            # 'context': ctx,
            'target': 'current'
        }


class StorageFileMixin(models.AbstractModel):
    _name = "storage.file.mixin"
    _description = "Storage File Mixin"

    def _link2product(self):
        model = self.env.context.get("active_model")
        record_ids = self.env.context.get("active_ids")
        tmpl_id = self.env.context.get("product_tmpl_id")
        map_storage = {
            "storage.image": "product.image.relation",
            "storage.media": "product.media.relation",
        }
        print(self.env.context)
        import pdb; pdb.set_trace()
        if record_ids:
            self.env[map_storage[model]].create(
                [{"image_id": img.id, "product_tmpl_id": tmpl_id}
                 for img in record_ids])
