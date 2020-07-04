from django.shortcuts import render,redirect,get_object_or_404

from django.http import request,JsonResponse
from django.template.loader import render_to_string

from orders.models import Order
from products.models import Product
from customers.models import Customer
from .forms import ProductForm

from .filters import ProductFilter

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q,Sum
from django.contrib.auth.decorators import login_required

from django.core import serializers






# def create(request):
#     form=ProductForm()
 
#     if(request.method=='POST'):
#         form=ProductForm(request.POST)
#         if(form.is_valid()):
#             form.save()
            
#         return redirect('/products/list?Product added ')
    
#     return render(request,'products/create.html',{'form':form})
    

@login_required(login_url = '/user/login/')
def index(request):   
    form = ProductForm()
    products=Product.objects.all()
    product_count = products.count()
    
    products = getPaginator(request,products)
    '''
    -->like form we render filterform
    -->we use get because we see result on same page 
    -->quertset because we have to see filter data that we search
    -->
    -->qs = queryset
    '''
  

    if(request.method=='POST'):
        form=ProductForm(request.POST)
        if(form.is_valid()):
            form.save()
            
        # return redirect('/products/list?Product added ')    
    context={'products':products,
           
             'form':form,
             'start':products.start_index(),
             'end':products.end_index(),
             'products_count':product_count
             }
    return render(request,'products/index.html',context)



def getPaginator(request,object):
    page = request.GET.get('page', 1)#means page  number 1
    paginator = Paginator(object, 5)
  
    try:
        products = paginator.page(page)
        
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        #if page is out of range show last page
        products = paginator.page(paginator.num_pages)
        
    return products#aflter pagination return object


    
def search(request):
    data = dict()
    field_value = request.GET.get('query')
    print(field_value)
    
    # products = Product.objects.all()
    # myFilter = ProductFilter(request.GET,queryset=products)
    # products = myFilter.qs
  
  
    if field_value:
        products = Product.objects.filter(
                                            Q(name__icontains=field_value)
                                           | Q(price__icontains=field_value) 
                                           | Q(description__icontains=field_value)
                                           | Q(quantity__icontains=field_value)
                                           | Q(id__icontains=field_value)
                                           | Q(category__icontains=field_value)
                                           )

        context = {'products': products}
            
        data['html_list'] = render_to_string('products/get_search_products.html',context,request=request)

   

        return JsonResponse(data)

    else:
        products = Product.objects.all()
       
        context = {'products': products}
        data['html_list'] = render_to_string('products/get_search_products.html',context,request=request)

        return JsonResponse(data)


def save_product_form(request, form, template_name):
   
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
            products = Product.objects.all()
            data['html_product_list'] = render_to_string('products/index.html', {
                #valid huda data goes to index.html else stay on template_name
                'products': products
            })
          
            
        else:
            data['form_is_valid'] = False
            
        '''if valid is false then go to  else {
            $("#modal-product .modal-content").html(data.html_form);}----> in products.js
            -->If value is invallid then without refreshing filled form it tells field is invalid in form 
            -->also apply for edit page and check edit data before submit and if error in editing then give same message like as adding data in form
          '''
            
    context = {'form': form}
    data['html_form'] = render_to_string(template_name, context, request=request)
    
    return JsonResponse(data)

def create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
    else:
        form = ProductForm()   
    return save_product_form(request,form,'products/create.html')


    '''whenever i come to create views with respective url then first ma form and template liyara save_product_form call hunxa.so,products/create show json data
          return JsonResponse(data) in save_product_form-- if request.method == 'POST': in create garda we pass form data in save_product_form and check for 
          validation of that data--in the same view retrieve save data and render to products/index.html
        '''
    



def edit(request, pid):
   
    pro = get_object_or_404(Product, pk=pid)
    
    if request.method == 'POST':#means when  submit in edit page
        form = ProductForm(request.POST, instance=pro)
        
    else:
        
        form = ProductForm(instance=pro)
    return save_product_form(request, form, 'products/update.html')


def delete_product(request, pid):
    data = dict()
    product = get_object_or_404(Product, pk=pid)
    
    if(request.method == 'POST'):#Use this when i confirm delete 
       
        product.delete()
        
        data['form_is_valid'] = True
        products = Product.objects.all()
        data['html_product_list'] = render_to_string('products/index.html',{'products':products})   
        
    else:
        
        context = {'pro': product}#this goes to action pro.id in delete.html
        data['html_form'] = render_to_string('products/delete.html', context, request=request)    
    return JsonResponse(data)




def productData(request,cid):
    
    productData = []
    cus = Customer.objects.get(pk=cid)
    # # customers = cus.values('name','created_at')

    order = cus.order_set.all()
    # order =  Order.objects.values('created_at','product__price')
    # productData = serializers.serialize('json',order)
    # productData = productData['name']
    
    
    for i in order:
        productData.append({i.customer.name:i.product.price})#right is value(can be value or string) and left(always string cannot be number) is keys in dict 
        # Date.append(i['created_at'])
        # productPrice.append(i['product__price'])
     
    print(productData)
    return JsonResponse(productData,safe=False)

# ------------------------------------------------------------------------------------------------------------------------------------
'''

def delete(request, pid):
 # cus=Customer.objects.get(id=pk)
    pro = get_object_or_404(Product,pk = pid)
    
                                     # print(f'I am instance of {{cus}}')
   
    if request.method=='POST':  #if i confirm in delete.html page otherwise dont need post request
        pro.delete()   #grab customer details and delete and after deleting moves to /customers/list/
     
        return redirect('product_app:list')
    
    return render(request,'products/delete.html',{'name':pro })#urls.py ko url render ma url search garxa at first




def edit(request, pid):    
    # pro=Product.objects.get(id=pk) #i get all value and show that value to next page
    pro = get_object_or_404(Product,pk = pid)
    form=ProductForm(instance=pro)
    
    if(request.method=='POST'):
        
        form=ProductForm(request.POST,instance=pro)
        if(form.is_valid()):
            form.save()
            messages.success(request,'Product is successfully updated.',extra_tags='alert')
            
        return redirect('product_app:list')#maila update.html ko save garda or post ma jada yo url ma redirect hunxa

    # else:
    #     form = ProductForm()
        
  
    return render(request,'products/update.html',{'form':form})
    
    '''
    
    
    









    
    
    


