# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountCommonReport(models.TransientModel):
    _name = "account.common.report"
    _description = "Account Common Report"

    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")
    target_move = fields.Selection(
        [('all', 'All Entries'), ('posted', 'Posted Entries')],
        string="Target Moves",
        required=True,
        default='all',
    )
    journal_ids = fields.Many2many('account.journal', string='Journals')
    amount_currency = fields.Boolean(string='With Currency')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )

    def _build_contexts(self, data):
        return {
            'journal_ids': data.get('journal_ids') or False,
            'state': data.get('target_move', 'all'),
            'date_from': data.get('date_from'),
            'date_to': data.get('date_to'),
            'strict_range': bool(data.get('date_from') or data.get('date_to')),
            'company_id': data.get('company_id'),
        }

    def check_report(self):
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': self.read(['date_from', 'date_to', 'journal_ids', 'target_move', 'company_id'])[0],
        }
        if hasattr(self, 'pre_print_report'):
            data = self.pre_print_report(data)
        data['form']['used_context'] = self._build_contexts(data['form'])
        return self._print_report(data)
