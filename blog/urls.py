from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from blog.views.views import (
    IndexTemplateView,
    # IndexView,
    # ProductDetailView,
    ProductDetailTemplateView,
    # ProductListView,
    ProductListTemplateView,
    ProductUpdateView,
    # CustomerListView,
    # CustomerDetailView,
    CustomerDetailTemplateView,
    DeleteCustomerView,
    # AddCustomerView,
    CreateCustomerView,
    CustomerUpdateView,
    CustomerExportView,
    ProductAddView,
    CustomerListView)

from blog.views.auth import (
                            LoginPageView,
                             LogoutPageView,
                             RegisterPageView,
                             sending_email,
                             verify_email_done,
                             verify_email_confirm,
                             verify_email_complete)

urlpatterns = [
    # For Product
    path('', IndexTemplateView.as_view(), name='index'),
    path('detail/<slug:slug>/', ProductDetailTemplateView.as_view(), name='product_details'),
    path('product-list/', ProductListTemplateView.as_view(), name='product_list'),
    path('product-add-url/',ProductAddView.as_view(), name='product_add_url'),
    path('update-product/<slug:slug>/', ProductUpdateView.as_view(), name='update_product'),

    # For Customer
    path('customer/', CustomerListView.as_view(), name='customers'),
    path('customers_detail/<int:pk>/', CustomerDetailTemplateView.as_view(), name='customer_detail'),
    path('delete/<int:pk>',DeleteCustomerView.as_view(),name='delete'),
    path('add-customer/', CreateCustomerView.as_view(), name = 'add_customers'),
    path('customer/<int:pk>/update', CustomerUpdateView.as_view(), name = 'update_customer' ),
    # Authentication's url
    path('login-page/', LoginPageView.as_view(), name='login'),
    # path('login-page/', LoginView.as_view(
    #     template_name = 'blog/auth/login.html',
    #     redirect_authenticated_user = True,
    #
    # ), name='login'),
    # path('logout-page/', LogoutView.as_view(), name='logout'),
    path('logout/', LogoutPageView.as_view(), name = 'logout'),
    path('register-page/', RegisterPageView.as_view(), name='register'),
    path('sending-email-url/',sending_email,name= 'sending_email'),

    # Verify email
    path('verify-email-done/', verify_email_done, name='verify_email_done'),
    path('verify-email-confirm/<uidb64>/<token>/', verify_email_confirm, name='verify-email-confirm'),
    path('verify-email/complete/', verify_email_complete, name='verify_email_complete'),

    # Exporting data
    path('customers-export-data-downloads/',CustomerExportView.as_view(), name = 'export_data')
]