# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from exceptions import ValueError

import base64

class TestOdooBackend(TransactionCase):

    def test_odoo_backend(self):
        """Simple case should work"""
        vals = {
            'name': 'odoo_back',
            'backend_type': 'odoo',
            'public_base_url': ''
        }
        backend = self.env['storage.backend'].create(vals)

        datas = base64.b64encode("random string")
        private_path = backend.store(
            "random_string", datas)

        # retrieve the data
        retrieved = backend.retrieve(private_path) 
        self.assertEqual(datas, retrieved)
