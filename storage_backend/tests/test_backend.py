# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from exceptions import ValueError

class TestBackend(TransactionCase):

    def test_default_backend(self):
        """Should raise an error if no implementation"""
        vals = {
            'name': 'doesntxists',
            'backend_type': 'doesntxists',
            'public_base_url': ''
        }
        try:
            self.env['storage.backend'].create(vals)
            self.assertTrue(False, "no backend implementation")
        except ValueError:
            self.assertTrue(True)

