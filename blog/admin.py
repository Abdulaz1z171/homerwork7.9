from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources

from blog.models import Product,  Image, Attribute,Customer,AttributeValue,ProductAttribute,User
from django.contrib.auth.models import Group
# Register your models here.



#admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Attribute)
# admin.site.register(Customer)
admin.site.register(AttributeValue)
admin.site.register(ProductAttribute)
#admin.site.register(User)
#admin.site.register(admin.CustomerAdmin)

admin.site.unregister(Group)

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email','first_name','is_superuser')

    search_fields = ('email',)

    list_filter = ('date_joined',)






@admin.register(Product)
class Product(admin.ModelAdmin):
    List_display = ("name", 'price', 'slug')
    #prepopulated_fields = {'slug': ('name',)}


@admin.register(Customer)
class CustomerModelAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['name','email','phone']


class CustomerResource(resources.ModelResource):
    class Meta:
     model = Customer
     fields = ('id','name','email','phone','billing_address','joined_date')
     export_oreder = ('id','name','email','billing_address','phone','joined_date')
    