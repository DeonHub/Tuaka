# from django import views
from django.urls import path
from . import views
# from . import context_processors

app_name = 'pay'

urlpatterns = [
    # path('', views.login, name="login"),
    path('<str:code>/', views.index, name="index"),
    path('<str:code>/account/<str:pid>/', views.account, name="account"),
    
    path('<str:code>/<str:pid>/make-payments/<int:pk>', views.makePayments, name="makePayments"),
    path('<str:code>/<str:mid>/view-payments/<str:pid>/', views.viewPayments, name="viewPayments"),

    path('ajax/load-amount-due/', views.load_amount_due, name='ajax_load_amount_due'),
    path('ajax/load-credit/', views.load_credit, name='ajax_load_credit'),
    path('ajax/load-bill/', views.load_bill, name='ajax_load_bill'),
    path('ajax/load-breakdown/', views.load_breakdown, name='ajax_load_breakdown'),
    path('ajax/load-outstanding/', views.load_outstanding, name='ajax_load_outstanding'),

    

    path('<str:code>/view-business/', views.viewBusiness, name="viewBusiness"),
    # path('<str:pid>/view-fee-type/', views.viewFeeType, name="viewFeeType"),
    # path('<str:pid>/edit-fee-type/<int:id>/', views.editFeeType, name='editFeeType'),
    # path('<str:pid>/delete-fee-type/<int:id>', views.deleteFeeType, name='deleteFeeType'),


    # path('<str:pid>/create-fee-items/', views.createFeeItems, name="createFeeItems"),
    # path('<str:pid>/view-fee-items/', views.viewFeeItems, name="viewFeeItems"),
    # path('<str:pid>/edit-fee-item/<int:id>', views.editFeeItem, name='editFeeItem'),
    # path('<str:pid>/delete-fee-item/<int:id>', views.deleteFeeItem, name='deleteFeeItem'),


    # path('<str:pid>/create-fee-description/', views.createFeeDescription, name="createFeeDescription"),
    # path('<str:pid>/view-fee-description/', views.viewFeeDescription, name="viewFeeDescription"),
    # path('<str:pid>/edit-fee-description/<int:id>', views.editFeeDescription, name='editFeeDescription'),
    # path('<str:pid>/delete-fee-description/<int:id>', views.deleteFeeDescription, name='deleteFeeDescription'),


    # path('<str:pid>/create-currency/', views.createCurrency, name="createCurrency"),
    # path('<str:pid>/view-currency/', views.viewCurrency, name="viewCurrency"),
    # path('<str:pid>/edit-currency/<int:id>', views.editCurrency, name='editCurrency'),
    # path('<str:pid>/delete-currency/<int:id>', views.deleteCurrency, name='deleteCurrency'),


    # path('<str:pid>/set-invoice-details/', views.setInvoiceDetails, name="setInvoiceDetails"),
    # path('<str:pid>/view-invoice-details/', views.viewInvoiceDetails, name="viewInvoiceDetails"),
    # path('<str:pid>/edit-invoice-details/<int:id>', views.editInvoiceDetails, name='editInvoiceDetails'),
    # path('<str:pid>/delete-invoice-details/<int:id>', views.deleteInvoiceDetails, name='deleteInvoiceDetails'),


    # path('<str:pid>/create-invoice/', views.createInvoice, name="createInvoice"),
    # path('<str:pid>/view-invoice/', views.viewInvoice, name="viewInvoice"),
    # path('<str:pid>/edit-invoice/<int:id>', views.editInvoice, name='editInvoice'),
    # # path('delete-invoice/<int:id>', views.deleteInvoice, name='deleteInvoice'),


    # path('create-donation/', views.createDonation, name="createDonation"),
    # path('view-donations/', views.viewDonations, name="viewDonations"),
    # path('view-donation/<int:id>', views.viewDonation, name="viewDonation"),
    # path('pay-donation/<int:id>', views.payDonation, name="payDonation"),


    # path('create-public-donation/', views.createPublicDonation, name="createPublicDonation"),
    # path('view-public-donations/', views.viewPublicDonations, name="viewPublicDonations"),
    # path('view-public-donation/<int:id>', views.viewPublicDonation, name="viewPublicDonation"),
    # path('edit-public-donation/<int:id>', views.editPublicDonation, name="editPublicDonation"),
    # path('pay-public-donation/<int:id>', views.payPublicDonation, name="payPublicDonation"),
    # path('public-donors/', views.publicDonors, name="publicDonors"),


    # path('assign-subscribers/', views.assignSubscriber, name="assignSubscriber"),
    # path('view-subscribers/', views.viewSubscribers, name="viewSubscribers"),
    # path('ajax/unassign_subscriber/', views.unassignSubscriber, name='unassignSubscriber'),
    # path('deactivated/', views.deactivated, name='deactivated'),



    # path('assign-payment/', views.assignPaymentDuration, name="assignPaymentDuration"),
    # path('assign-donation/<int:pk>', views.assignDonation, name="assignDonation"),
    # path('<str:pid>/assign-payments/<int:pk>', views.assignPaymentsDuration, name="assignPaymentsDuration"),
    # path('<str:pid>/view-payment-details/', views.viewPaymentDuration, name="viewPaymentDuration"),
    # path('<str:pid>/delete-invoice/<int:id>', views.deletePaymentDuration, name='deletePaymentDuration'),




    # path('ajax/load-groups/', views.load_groups, name='ajax_load_groups'),
    # path('ajax/load-subgroups/', views.load_subgroups, name='ajax_load_subgroups'),

    # path('ajax/load-items/', views.load_items, name='ajax_load_items'),
    # path('ajax/load-amount-due/', views.load_amount_due, name='ajax_load_amount_due'),
    # path('ajax/load-credit/', views.load_credit, name='ajax_load_credit'),
    # path('ajax/load-invoice/', views.load_invoice, name='ajax_load_invoice'),
    # path('ajax/load_balance/', views.load_balance, name='ajax_load_balance'),
    # path('ajax/load_fee/', views.load_fee, name='ajax_load_fee'),
    # path('<str:pid>/ajax/delete_payment/', views.delete_payment, name='ajax_delete_payment'),
    # path('<str:pid>/ajax/delete_assigned/', views.delete_assigned, name='ajax_delete_assigned'),
    # path('<str:pid>/ajax/delete_invoice/', views.delete_invoice, name='ajax_delete_invoice'),

    # # path('ajax/period/', views.period, name='ajax_period'),
    # # path('ajax/period/', context_processors.period, name='ajax_period'),
    # path('send-sms/', views.send_sms, name='send_sms'),
    # path('send-mail/<int:pk>', views.send_mail, name='send_mail'),
    # path('logout/<str:pid>/', views.logout, name='logout'),
    # path('<str:pid>/view-members/', views.viewMembers, name='viewMembers'),
    # path('thank-you/', views.thank_you, name='thank_you'),
    # path('activity-log/<str:pid>/', views.viewActivityLog, name='viewActivityLog'),

    # path('make-payment/', views.makePayment, name="makePayment"),
    # path('<str:pid>/make-payments/<int:pk>', views.makePayments, name="makePayments"),
    # path('<str:pid>/view-assigned/<int:pk>', views.viewAssigned, name="viewAssigned"),
    # path('<str:pid>/view-payments/', views.viewPayments, name="viewPayments"),
    # path('<str:pid>/invoice-details-view/<int:pk>', views.invoice_details_view, name="invoice_details_view"),
    # path('donors_csv/', views.donors_csv, name="donors_csv"),
    # path('subscribers_csv/', views.subscribers_csv, name="subscribers_csv"),
    # path('<str:pid>/donation-details-view/<int:pk>', views.donation_details_view, name="donation_details_view"),
    # path('<str:pid>/view-details/<int:pk>', views.viewDetails, name="viewDetails"),
    # path('<str:pid>/view-invoices/<int:pk>', views.viewInvoices, name="viewInvoices"),
    # path('<str:pid>/view-organization/<int:pk>', views.viewOrganizationDetail, name="viewOrganizationDetail"),
    # path('<str:pid>/profile/', views.viewProfile, name="viewProfile"),
    # path('client-profile/<int:id>', views.viewClientProfile, name="viewClientProfile"),


    # path('send-sms/', views.balances, name="balances"),

    # path('create-invoice-it/', views.createInvoiceType, name="createInvoiceType"),
    # path('home/', views.home, name="home"),
]



