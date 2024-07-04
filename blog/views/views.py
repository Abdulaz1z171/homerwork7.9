import csv
import json


from django.shortcuts import render
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView

from ..forms import CustomerModelForm, ProductListModelForm
from django.http import HttpResponse
from openpyxl import Workbook

from blog.models import Product
from django.db.models import Q
from ..models import Customer
from django.shortcuts import render, redirect
from ..admin import CustomerResource
# from django.shortcuts import reverse_lazy
from django.views.generic.edit import UpdateView, CreateView, DeleteView


# Product view section

# class based view ///////////////////////////////////////////////////////////////

class IndexTemplateView(TemplateView):
    template_name = 'blog/product/index.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        paginator = Paginator(products,2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context

# class IndexView(View):
#     def get(self,request):
#         products = Product.objects.all()
#         paginator = Paginator(products,2)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         context = {
#             'page_obj' : page_obj,
#         }
#         return render(request,'blog/product/index.html',context)
#

# def index(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 2)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'page_obj': page_obj,
#     }
#     return render(request, 'blog/product/index.html', context)

class ProductDetailTemplateView(TemplateView):
    template_name = 'blog/product/product-details.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug = kwargs['slug'])
        attributes = product.get_attributes()
        context['attributes'] = attributes
        context['product'] = product
        context['slug'] = kwargs['slug']
        return context


# class ProductDetailView(View):
#     def get(self,request,slug):
#         product = Product.objects.get(slug=slug)
#         attributes = product.get_attributes()
#         context = {
#             'product' : product,
#             'attributes' : attributes
#         }
#         return render(request,'blog/product/product-details.html',context)

# def product_detail(request, slug):
#     product = Product.objects.get(slug=slug)
#     attributes = product.get_attributes()
#
#     context = {
#         'product': product,
#         'attributes': attributes
#     }
#     return render(request, 'blog/product/product-details.html', context)


class ProductListTemplateView(TemplateView):
    template_name = 'blog/product/product-list.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all()
        paginator = Paginator(products,2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


# class ProductListView(View):
#     def get(self,request):
#         products = Product.objects.all()
#         paginator = Paginator(products, 3)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#
#         context = {
#             'page_obj': page_obj,
#
#         }
#         return render(request, 'blog/product/product-list.html', context)


# def product_list(request):
#     products = Product.objects.all()
#     paginator = Paginator(products, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'page_obj': page_obj,
#
#     }
#     return render(request, 'blog/product/product-list.html', context)


class ProductAddView(View):
    def get(self,request):
        form = ProductListModelForm()
        return render(request,'blog/product/product-add.html',{'form': form})
    def post(self,request):
        form = ProductListModelForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'blog/product/product-add.html')

class ProductUpdateView(View):
    def get(self,request,slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(instance=product)
        return render(request, 'blog/product/update-product.html',{'form':form})
    def post(self,request,slug):
        product = Product.objects.get(slug=slug)
        form = ProductListModelForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('index')
        return render(request, 'blog/product/update-product.html',{'form':form})


#  For Customers
class CustomerListView(ListView):
    model = Customer
    template_name = 'blog/customer/customers.html'
    paginate_by = 2

    def get_queryset(self):
        self.queryset = super(CustomerListView, self).get_queryset()
        search_query = self.request.GET.get('search')
        if search_query:
            self.queryset = Customer.objects.filter(
                Q(name__icontains=search_query) | (Q(email__icontains=search_query)))
        else:
            self.queryset = Customer.objects.all()
        return self.queryset




# class CustomerListTemplateView(TemplateView):
#     template_name = 'blog/customer/customers.html'
#     def get_context_data(self,**kwargs):
#         context = super().get_context_data(**kwargs)
#         customers = Customer.objects.all()
#         dataset = CustomerResource().export(customers)
#         format = self.request.GET.get('format')
#         if format == 'xls':
#             ds = dataset.xls
#         elif format == 'csv':
#             ds = dataset.csv
#         else:
#             ds = dataset.json
#
#         paginator = Paginator(customers,3)
#         page_number = self.request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#         search_query = self.request.GET.get('search')
#         if search_query:
#             page_obj = Customer.objects.filter(Q(name__icontains=search_query) | (Q(email__icontains=search_query)))
#         else:
#             customers = Customer.objects.all()
#
#         context['page_obj'] = page_obj
#         context['format'] = format
#         return context

# class CustomerListView(View):
#      def get(self, request):
#          customers = Customer.objects.all()
#          dataset = CustomerResource().export(customers)
#          format = request.GET.get('format')
#          if format == 'xls':
#              ds = dataset.xls
#          elif format == 'csv':
#              ds = dataset.csv
#          else:
#              ds = dataset.json
#          paginator = Paginator(customers, 5)
#          page_number = request.GET.get("page")
#          page_obj = paginator.get_page(page_number)
#          search_query = request.GET.get('search')
#          if search_query:
#              page_obj = Customer.objects.filter(Q(name__icontains=search_query) | (Q(email__icontains=search_query)))
#          else:
#              customers = Customer.objects.all()
#          context = {
#
#              'page_obj': page_obj,
#              'format': format
#          }
#          return render(request, 'blog/customer/customers.html', context)


# def customers(request):
#     customers = Customer.objects.all()
#     dataset = CustomerResource().export(customers)
#     format = request.GET.get('format')
#     if format == 'xls':
#         ds = dataset.xls
#     elif format == 'csv':
#         ds = dataset.csv
#     else:
#         ds = dataset.json
#     paginator = Paginator(customers, 5)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#     search_query = request.GET.get('search')
#     if search_query:
#         page_obj= Customer.objects.filter(Q(name__icontains=search_query)|(Q(email__icontains = search_query)))
#     else:
#         customers = Customer.objects.all()
#     context = {
#
#         'page_obj': page_obj,
#         'format' : format
#     }
#     return render(request, 'blog/customers.html', context)


# <<<< Class Based View with CreateView>>>>

class CreateCustomerView(CreateView):
    model = Customer
    template_name = 'blog/customer/add-customer.html'
    fields = ('name', 'email', 'phone','billing_address',)
    success_url = reverse_lazy('customers')

# class AddCustomerView(View):
#     def get(self, request):
#         form = CustomerModelForm()
#         context = {
#
#             'form': form
#         }
#         return render(request, 'blog/customer/add-customer.html', context)
#     def post(self,request):
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#
#         context = {
#
#             'form': form
#         }
#         return render(request, 'blog/customer/add-customer.html', context)


# def add_customer(request):
#
#     form = CustomerModelForm()
#     if request.method == 'POST':
#         form = CustomerModelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('customers')
#
#     context = {
#
#         'form': form
#     }
#     return render(request, 'blog/customer/add-customer.html', context)


class CustomerDetailTemplateView(TemplateView):
    template_name = 'blog/customer/customer-details.html'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(pk = self.kwargs['pk'])
        context['customer'] = customer
        return context


# class CustomerDetailView(View):
#     def get(self,request,pk):
#         customers = Customer.objects.get(id=pk)
#         context = {
#            'customers': customers
#         }
#         return render(request, 'blog/customer/customer-details.html', context)


# def customers_detail(request, pk):
#     customers = Customer.objects.get(id=pk)
#     context = {
#         'customers': customers
#     }
#     return render(request, 'blog/customer/customer-details.html', context)

class DeleteCustomerView(DeleteView):
    model = Customer
    template_name = 'blog/customer/delete.html'
    success_url = reverse_lazy('customers')


# <<< Class Based View >>>

# class DeleteCustomerView(View):
#     def get(self,request,pk):
#         customer = Customer.objects.get(id=pk)
#         if customer :
#             customer.delete()
#             return redirect('customers')
#         context = {
#             'customer' : customer
#         }
#         return render(request, 'blog/customer/customer-details.html',context)

# <<< Function Based View simple view>>>
# def delete_customer(request, pk):
#     customer = Customer.objects.filter(id=pk).first()
#     if customer:
#         customer.delete()
#         return redirect('customers')
#     context = {
#         'customer': customer
#
#     }
#     return render(request, 'blog/customer/customer-details.html', context)


class CustomerUpdateView(UpdateView):
    model  = Customer
    template_name = 'blog/customer/update.html'
    context_object_name = 'customer'
    fields = ('name','email','phone','billing_address',)


    def get_success_url(self):
        return reverse_lazy('customer_detail',kwargs = {'pk': self.object.id})

#  <<<<<Class based simple View>>>>
# class UpdateCustomerView(View):
#     def get(self,request,pk):
#         customer = Customer.objects.get(id=pk)
#         form = CustomerModelForm(instance=customer)
#         context = {
#                 'form': form,
#                 'customer': customer
#             }
#         return render(request, 'blog/customer/update.html', context)
#
#     def post(self,request,pk):
#         customer = Customer.objects.get(id=pk)
#         form = CustomerModelForm(request.POST, instance=customer)
#         if form.is_valid():
#             form.save()
#             return redirect('customer_detail',pk)
#         context = {
#                 'form': form,
#                 'customer': customer
#             }
#         return render(request, 'blog/customer/update.html', context)


# <<<< Functiond based view>>>>
# def update_customer(request,pk):
#     customer = Customer.objects.get(id = pk)
#     form = CustomerModelForm(instance=customer)
#     if request.method =='POST':
#            form = CustomerModelForm(request.POST, request.FILES, instance=customer)
#            if form.is_valid():
#                form.save()
#                return redirect('customers_details', pk)
#
#     context = {
#         'form': form,
#         'customer': customer
#     }
#     return render(request, 'blog/customer/update.html', context)
               


# def export_data(request):
#     format = request.GET.get('format','csv')
#     if format == 'csv':
#         response = HttpResponse(content_type = 'txt/csv')
#         response['Content-Disposition'] = 'attachment; filename = "customers.csv" '
#         writer = csv.writer(response)
#         writer.writerow(['id','name','phone','email','billing_address'])
#         for customer in Customer.objects.all():
#             writer.writerow([customer.id,customer.name,customer.phone,customer.email, customer.billing_address])
#
#     elif format == 'json':
#         response = HttpResponse(content_type = 'aplication/json')
#
#         data = list(Customer.objects.values('id','name','phone','email','billing_address'))
#         response.content = json.dumps(data,indent=4)
#         response['Content-Disposition'] = 'attachment; filename = "customers.json" '
#
#     elif format == 'xlsx':
#         response = HttpResponse(content_type='application/ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="customers.xlsx" '
#         wb = Workbook()
#         ws = wb.active
#         ws.title = "Customers"
#
#         # Add headers
#         headers = ["id", "name", "phone","email","billing_address"]
#         ws.append(headers)
#
#         # Add data from the model
#         customers = Customer.objects.all()
#         for customer in customers:
#             ws.append([customer.id,customer.name,customer.phone,customer.email,customer.billing_address])
#
#         # Save the workbook to the HttpResponse
#         wb.save(response)
#
#
#     else:
#         response = HttpResponse(status = 404)
#         response.content = ('Bad request')
#     return response
#
#
#


class CustomerExportView(View):
    def get(self,request):
        format = request.GET.get('format', 'csv')
        if format == 'csv':
            response = HttpResponse(content_type='txt/csv')
            response['Content-Disposition'] = 'attachment; filename = "customers.csv" '
            writer = csv.writer(response)
            writer.writerow(['id', 'name', 'phone', 'email', 'billing_address'])
            for customer in Customer.objects.all():
                writer.writerow([customer.id, customer.name, customer.phone, customer.email, customer.billing_address])

        elif format == 'json':
            response = HttpResponse(content_type='aplication/json')

            data = list(Customer.objects.values('id', 'name', 'phone', 'email', 'billing_address'))
            response.content = json.dumps(data, indent=4)
            response['Content-Disposition'] = 'attachment; filename = "customers.json" '

        elif format == 'xlsx':
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename="customers.xlsx" '
            wb = Workbook()
            ws = wb.active
            ws.title = "Customers"

            # Add headers
            headers = ["id", "name", "phone", "email", "billing_address"]
            ws.append(headers)

            # Add data from the model
            customers = Customer.objects.all()
            for customer in customers:
                ws.append([customer.id, customer.name, customer.phone, customer.email, customer.billing_address])

            # Save the workbook to the HttpResponse
            wb.save(response)


        else:
            response = HttpResponse(status=404)
            response.content = ('Bad request')
        return response

