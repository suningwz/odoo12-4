# -*- coding: utf-8 -*-

from odoo import models, api, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_credit_limit_exceeded = fields.Boolean("Credit Limit Exceeded", store=True, compute="_compute_is_credit_limit_exceeded")
    total_quotes = fields.Float("Total Quotes", compute='_total_quotes', store=True)
    current_credit = fields.Float("Current Credit", compute='_current_credit', store=True)

    @api.depends('sale_order_ids', 'sale_order_ids.state', 'sale_order_ids.invoice_status', 'sale_order_ids.amount_total')
    def _total_quotes(self):
        for rec in self:
            rec.total_quotes = sum(rec.sale_order_ids.filtered(lambda so: so.invoice_status in ['to invoice', 'no']).mapped('amount_total'))

    @api.depends('total_quotes', 'total_due')
    def _current_credit(self):
        for rec in self:
            rec.current_credit = rec.total_due + rec.total_quotes

    @api.depends('credit_limit', 'current_credit')
    def _compute_is_credit_limit_exceeded(self):
        for rec in self:
            rec.is_credit_limit_exceeded = rec.current_credit > rec.credit_limit
