# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    'name': "Storage backend load file",
    'description': """Sorage submodule used to load every file of a storage
    backend as Odoo attachments""",
    'author': 'ACSONE SA/NV',
    'website': "http://acsone.eu",
    'category': 'Storage',
    'version': '10.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'component',
        'storage_backend',
        'document',
    ],
    'data': [
        'data/ir_cron.xml',
        'views/ir_attachment.xml',
        'views/storage_backend.xml',
    ],
}
