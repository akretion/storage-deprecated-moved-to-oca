# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import datetime
from os import path
from base64 import b64encode, b64decode
import hashlib
from odoo.addons.component.tests.common import TransactionComponentCase
from odoo import api, fields
PATH = path.join(path.dirname(__file__), "files/")


class TestStorageBackend(TransactionComponentCase):
    """
    Tests for storage.backend
    """

    def setUp(self):
        super(TestStorageBackend, self).setUp()
        file_names = self.file_names = [
            'demo1.txt',
            'demo2.txt',
            'demo3.txt',
        ]
        self.storage_obj = self.env['storage.backend']
        self.attachment_obj = self.env['ir.attachment']
        self.storage = self.storage_obj.create({
            'name': 'Unit test',
            'backend_type': 'filesystem',
            'directory_path': '/tmp',
            'conservation_days': 1,
        })

        @api.multi
        def _get_file_base64(self):
            """
            Patch the real method to use current demo files without remove them
            :param self:
            :return: tuple (str, b64)
            """
            for file_name in file_names:
                with open(PATH + file_name, mode='r') as demo_file:
                    yield file_name, b64encode(demo_file.read())

        @api.multi
        def _get_removal_date(self):
            """
            Patch the real method to change the removal date
            :return: date (str)
            """
            today = fields.Date.from_string(fields.Date.today())
            # Put date in the future to force delete
            removal_date = today + datetime.timedelta(days=15)
            return fields.Date.to_string(removal_date)

        self.storage_obj._patch_method('_get_file_base64', _get_file_base64)
        self.storage_obj._patch_method('_get_removal_date', _get_removal_date)
        self.addCleanup(self.storage_obj._revert_method, '_get_file_base64')
        self.addCleanup(self.storage_obj._revert_method, '_get_removal_date')

    def test_attachment_created1(self):
        """
        Test if attachments are correctly created, based on directory content
        :return:
        """
        attachments = self.storage._auto_load_content()
        self.assertEquals(len(attachments), len(self.file_names))
        file_names = self.file_names
        for attachment in attachments:
            self.assertTrue(attachment.from_storage_backend)
            self.assertEquals(attachment.res_model, self.storage._name)
            self.assertEquals(attachment.res_id, self.storage.id)
            self.assertIn(attachment.name, self.file_names)
            file_name = file_names.pop(file_names.index(attachment.name))
            with open(PATH + file_name, mode='r') as demo_file:
                content = demo_file.read()
            attachment_content = b64decode(attachment.datas)
            hash1 = hashlib.md5()
            hash1.update(content)
            hexa1 = hash1.hexdigest()
            hash2 = hashlib.md5()
            hash2.update(attachment_content)
            hexa2 = hash2.hexdigest()
            self.assertEquals(hexa1, hexa2)
        # Ensure all files are loaded as attachment
        self.assertFalse(file_names)
        return

    def test_purge1(self):
        """
        Test if attachments are correctly created, based on directory content
        :return:
        """
        existing_attachments = self.attachment_obj.search([])
        attachments = self.attachment_obj.browse()
        for file_name in self.file_names:
            with open(PATH + file_name, mode='r') as demo_file:
                content = demo_file.read()
            attachments |= self.storage._create_attachment(
                file_name, b64encode(content))
        self.storage._purge_attachment()
        # Ensure correctly deleted
        self.assertFalse(attachments.exists())
        attachments_after = self.attachment_obj.search([])
        # Ensure nothing else deleted from attachments
        self.assertEquals(existing_attachments, attachments_after)
        return
