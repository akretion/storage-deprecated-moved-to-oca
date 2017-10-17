# -*- coding: utf-8 -*-
# © <YEAR(S)> <AUTHOR(S)>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase
from exceptions import ValueError
from odoo.exceptions import AccessError
import os
import base64

class TestFSBackend(TransactionCase):

    def setUp(self):
        super(TestFSBackend, self).setUp()
        if os.path.isdir(
            '%s/test_fs_dir' % self.env['storage.backend']._basedir()):
            self.assertTrue(False, "Can't run tests if test directory exists")

    def tearDown(self):
        path = '%s/test_fs_dir' % self.env['storage.backend']._basedir()
        if os.path.isdir(path):
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                # there is no subdir
            os.rmdir(path)
        super(TestFSBackend, self).tearDown()

    def test_simple(self):
        """It should work in simple case"""
        vals = {
            'name': 'fs_bak',
            'backend_type': 'filestore',
            'public_base_url': '',
            'filestore_base_path': 'test_fs_dir',
            'filestore_public_base_url': '',
        }
        backend = self.env['storage.backend'].create(vals)

        datas = base64.b64encode("random string")
        private_path = backend.store(
            "random_string", datas)

        # retrieve the data
        retrieved = backend.retrieve(private_path) 
        self.assertEqual(datas, retrieved, 'black box')


    def test_ensure_fullpath(self):
        """It should constraint write to a dir"""
        vals = {
            'name': 'fs_bak',
            'backend_type': 'filestore',
            'public_base_url': '',
            'filestore_base_path': 'test_fs_dir',
            'filestore_public_base_url': '',
        }
        backend = self.env['storage.backend'].create(vals)

        # fetch the file
        self.assertTrue(
            backend
                ._fullpath('where_i_want')
                .endswith('storage/test_fs_dir/where_i_want')
        )

        #self.assertTrue(
        #    backend
        #        ._fullpath('../with_double_dot')
        #        .endswith('storage/test_fs_dir/with_double_dot')
        #    , 'it should survive basic escape ../'
        #)
        try:
            backend._fullpath('/with_slash')
            self.assertTrue(False, 'it should raise')
        except AccessError:
            self.assertTrue(True)

        print backend._fullpath('../../../outside')
        try:
            backend._fullpath('../../../outside')
            .endswith('storage/test_fs_dir/outside')
            , 'it should survive basic escape ../../'
        )

    def test_overwrite_files(self):
        """It should not overwrite files"""
        vals = {
            'name': 'fs_bak',
            'backend_type': 'filestore',
            'public_base_url': '',
            'filestore_base_path': 'test_fs_dir',
            'filestore_public_base_url': '',
        }
        backend = self.env['storage.backend'].create(vals)

        datas = base64.b64encode("random string")
        private_path = backend.store(
            "random_string", datas)
        try:
            private_path2 = backend.store(
            "random_string", datas)
            self.assertTrue(False, 'it should raise something')
        except AccessError:
            self.assertTrue(True)

        try:
            private_path3 = backend.store(
            "random_string", datas, erase_file=True)
            self.assertTrue(True, 'it should work with force mode')
        except AccessError:
            self.assertTrue(False, 'it should raise something')
