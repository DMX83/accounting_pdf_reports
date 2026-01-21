# -*- coding: utf-8 -*-

from odoo import models


class AccountCommonJournalReport(models.TransientModel):
    _name = "account.common.journal.report"
    _inherit = "account.common.report"
    _description = "Account Common Journal Report"
