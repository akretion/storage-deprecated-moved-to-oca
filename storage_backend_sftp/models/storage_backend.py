# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StorageBackend(models.Model):
    _inherit = "storage.backend"

    backend_type = fields.Selection(selection_add=[("sftp", "SFTP")])
    sftp_password = fields.Char(string="Password")
    sftp_login = fields.Char(
        string="Login", help="Login to connect to sftp server", sparse="data"
    )
    sftp_server = fields.Char(string="Host", sparse="data")
    sftp_port = fields.Integer(string="Port", default=22, sparse="data")
    sftp_auth_method = fields.Selection(
        string="Authentification Method",
        selection=[("pwd", "Password"), ("ssh_key", "Private key")],
        default="pwd",
        required=True,
    )

    @property
    def _server_env_fields(self):
        base_fields = super()._server_env_fields
        sftp_fields = {
            "sftp_server": {},
            "sftp_port": {'getter': "getint"},
            "sftp_login": {},
            "sftp_password": {},
            "sftp_auth_method": {}
        }
        sftp_fields.update(base_fields)
        return sftp_fields
