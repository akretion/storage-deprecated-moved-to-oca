# -*- coding: utf-8 -*-
# Copyright 2019 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import datetime
import logging
from odoo import api, fields, models
from odoo.addons.queue_job.job import job
_logger = logging.getLogger(__name__)


class StorageBackend(models.Model):
    _inherit = 'storage.backend'

    conservation_days = fields.Integer(
        default=30,
        help="How many days attachments loaded must be saved into the system."
             "\nUse a negative value to disable the feature",
    )
    auto_delete = fields.Boolean(
        default=True,
        help="After downloading the file, delete it automatically",
    )

    @api.multi
    def _create_attachment(self, name, data):
        """
        Create the attachment with given data and attached on
        the current record
        :param name: str
        :param data: str (b64 encoded!)
        :return: ir.attachment
        """
        self.ensure_one()
        values = {
            'name': name,
            'datas': data,
            'datas_fname': name,
            'res_model': self._name,
            'res_id': self.id,
            'from_storage_backend': True,
        }
        return self.env['ir.attachment'].create(values)

    @api.multi
    def _get_file_base64(self):
        """
        Load every file (1 by 1) to have the name and the base64 value.
        Once the file is read, this one is automatically deleted.
        Use yield to avoid loading every file in memory.
        :return: list of tuple (str, str)
        """
        self.ensure_one()
        file_names = self._list()
        for file_name in file_names:
            yield file_name, self._get_b64_data(file_name)
            if self.auto_delete:
                self._delete(file_name)

    @api.multi
    @job(default_channel='root.backend_load.import')
    def _auto_load_content(self):
        """
        Load content of storage backend and create attachment for each file
        found
        :return: ir.attachment recordset
        """
        self.ensure_one()
        attachment_obj = self.env['ir.attachment']
        attachments = attachment_obj.browse()
        for file_name, file_b64 in self._get_file_base64():
            attachments |= self._create_attachment(file_name, file_b64)
        _logger.info(
            "%s documents loaded from the backend storage", len(attachments))
        return attachments

    @api.model
    def launch_auto_load_content(self, ids=False):
        """
        Launch the automatic load of content/files
        :param ids: list of int
        :return:
        """
        if ids:
            descr = "Load files from storage backend"
            for record in self.browse(ids):
                record.with_delay(description=descr)._auto_load_content()

    @api.multi
    def _get_removal_date(self):
        """
        Get the removal date depending on the current date and the
        conservation_days
        :return: date (str)
        """
        self.ensure_one()
        today = fields.Date.from_string(fields.Date.today())
        removal_date = today - datetime.timedelta(days=self.conservation_days)
        return fields.Date.to_string(removal_date)

    @api.multi
    @job(default_channel='root.backend_load.purge')
    def _purge_attachment(self):
        """
        Purge attachment loaded.
        Only attachment who comes from current backend and where the
        create_date < number of days (conservation_days)
        If the conservation_days < 0, then we don't have to delete attachments
        :return: bool
        """
        self.ensure_one()
        if self.conservation_days < 0:
            return True
        removal_date = self._get_removal_date()
        domain = [
            ('res_model', '=', self._name),
            ('res_id', '=', self.id),
            ('from_storage_backend', '=', True),
            ('create_date', '<', removal_date),
        ]
        attachments = self.env['ir.attachment'].search(domain)
        if attachments:
            _logger.info(
                "Delete %s attachment from the Storage backend",
                len(attachments))
            attachments.unlink()
        else:
            _logger.info("No attachment to delete found from the Storage "
                         "backend")
        return True

    @api.model
    def launch_purge(self, ids=False):
        """
        Launch the purge (to clean old files)
        :param ids: list of int
        :return:
        """
        if ids:
            descr = "Purge old files from storage backend"
            for record in self.browse(ids):
                record.with_delay(description=descr)._purge_attachment()
