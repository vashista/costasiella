from django.utils.translation import gettext as _
from django.utils import timezone

from django.db import models

from .finance_costcenter import FinanceCostCenter
from .finance_glaccount import FinanceGLAccount
from .finance_invoice import FinanceInvoice
from .finance_taxrate import FinanceTaxRate

class FinanceInvoiceItem(models.Model):
    finance_invoice = models.ForeignKey(FinanceInvoice, on_delete=models.CASCADE)
    line_number = models.PositiveSmallIntegerField(default=1)
    product_name = models.CharField(max_length=255)
    description = models.TextField(default="")
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    finance_tax_rate = models.ForeignKey(FinanceTaxRate, on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    finance_glaccount = models.ForeignKey(FinanceGLAccount, on_delete=models.CASCADE, null=True)
    finance_costcenter = models.ForeignKey(FinanceCostCenter, on_delete=models.CASCADE, null=True)


    def __str__(self):
        return self.finance_invoice.invoice_number + ' line: ' + self.line_number + ' ' + self.product_name

    
    #TODO: Calculate subtotal, vat and total on save :)


# def define_invoices_items():
#     ac_query = (db.accounting_costcenters.Archived == False)
#     ag_query = (db.accounting_glaccounts.Archived == False)

#     db.define_table('invoices_items',
#         Field('invoices_id', db.invoices,
#             readable=False,
#             writable=False),
#         Field('Sorting', 'integer',
#             readable=False,
#             writable=False),
#         Field('ProductName',
#             requires=IS_NOT_EMPTY(error_message = T("Enter product name")),
#             label   =T("Product Name")),
#         Field('Description', 'text',
#             label=T("Description")),
#         Field('Quantity', 'double',
#             requires=IS_FLOAT_IN_RANGE(-100000, 1000000, dot=".",
#                      error_message=T("Enter a number, decimals use '.'")),
#             default=1,
#             label=T("Quantity")),
#         Field('Price', 'double',
#             represent=represent_float_as_amount,
#             default=0,
#             label=T("Price")),
#         Field('tax_rates_id', db.tax_rates,
#             requires=IS_EMPTY_OR(IS_IN_DB(db(),
#                                   'tax_rates.id',
#                                   '%(Name)s')),
#             represent=represent_tax_rate,
#             label=T("Tax rate")),
#         Field('TotalPriceVAT', 'double',
#             compute=lambda row: row.Price * row.Quantity,
#             represent=represent_float_as_amount),
#         Field('VAT', 'double',
#             compute=compute_invoice_item_vat,
#             represent=represent_float_as_amount),
#         Field('TotalPrice', 'double',
#             compute=compute_invoice_item_total_price,
#             represent=represent_float_as_amount),
#         Field('accounting_glaccounts_id', db.accounting_glaccounts,
#               requires=IS_EMPTY_OR(IS_IN_DB(db(ag_query),
#                                             'accounting_glaccounts.id',
#                                             '%(Name)s')),
#               represent=represent_accounting_glaccount,
#               label=T('G/L Account'),
#               comment=T('General ledger account ID in your accounting software')),
#         Field('accounting_costcenters_id', db.accounting_costcenters,
#             requires=IS_EMPTY_OR(IS_IN_DB(db(ac_query),
#                                           'accounting_costcenters.id',
#                                           '%(Name)s')),
#             represent=represent_accounting_costcenter,
#             label=T("Cost center")),