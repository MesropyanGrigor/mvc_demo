import glob
import pandas as pd

from django.shortcuts import render, get_object_or_404
from .forms import FormUser, FormOrder, FormOrderItem
from .models import User, Order, OrderItem
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.core.exceptions import  ObjectDoesNotExist


def order(request):
    """Making and order and keeping it in the database"""
    if request.method == 'POST':
        user_form = FormUser(request.POST)
        order_form = FormOrder(request.POST)
        orderitem_form = FormOrderItem(request.POST) 
        #v_bool = user_form.is_valid() + order_form.is_valid() + orderitem_form.is_valid()
        #Doing this for checking all form validations
        #if user_form.is_valid() and order_form.is_valid() and orderitem_form.is_valid():
        #if user_form.is_valid():
        #    if order_form.is_valid():
        #        if orderitem_form.is_valid():
        v_bool = user_form.is_valid()
        v_bool &= order_form.is_valid()
        v_bool &= orderitem_form.is_valid()
        data = {}
        if v_bool:
            user_inst = user_form.save(commit=False)
            order_inst = order_form.save(commit=False)
            order_inst.user = user_inst
            orderitem_inst = orderitem_form.save(commit=False)
            orderitem_inst.order = order_inst
            user_form.save()
            order_form.save()
            orderitem_form.save()
            #return HttpResponse("<h1>Order is submitted</h1>")
        #messages.success(request, "Order is successfully added", extra_tags='alert')
        #if user_form._errors or order_form._errors or orderitem_form._errors:
        else:
            for err_ in [user_form._errors, order_form._errors, orderitem_form._errors]:
                if err_:
                    data.update(err_)
        #breakpoint()
        #word = '<br>&emsp;&emsp;&emsp;&emsp;'
        #errs = word + word.join([f'[{key}] : {row}' for key, dt in data.items() for row in dt ])
        #return HttpResponse(f"<h1>Errors:{errs}</h1>")
        return render(request, 'errors.html', {'data' : data})
        #return JsonResponse(data, safe=False)
    else:
        return render(request, 'order.html',
                      {'data': {**FormUser.Meta.name2field, 
                                **FormOrderItem.Meta.name2field}})

def add_data(data_):
    user_form = FormUser(data=data_)
    order_form = FormOrder(data=data_)
    orderitem_form = FormOrderItem(data=data_) 
    if user_form.is_valid():
        user_inst = user_form.save(commit=False)
    if order_form.is_valid():
        order_inst = order_form.save(commit=False)
        order_inst.user = user_inst
    if orderitem_form.is_valid():
        orderitem_inst = orderitem_form.save(commit=False)
        orderitem_inst.order = order_inst
    user_form.save()
    order_form.save()
    orderitem_form.save()

def get_rows_in_str():
    """Providing all data in the database as a list of list,
        each list is representing a row in the database"""
    rows = []
    for row in OrderItem.objects.all():
        row_  = []
        for field_ in FormOrderItem.Meta.fields:
            row_.append(getattr(row, field_))
        for field_ in FormOrder.Meta.fields:
            row_.append(getattr(row.order, field_))
        for field_ in FormUser.Meta.fields:
            row_.append(getattr(row.order.user, field_))
        rows.append([str(i_) for i_ in row_])
    return rows

def get_list():
    dict_0 = {**FormUser.Meta.name2field, 
              **FormOrderItem.Meta.name2field}
    new_dict = {value: key for key, value in dict_0.items()}  # swaping dict
    return  [new_dict[field] for field in 
             FormOrderItem.Meta.fields +  FormOrder.Meta.fields + FormUser.Meta.fields]

def order_list(request):
    """Showing all data of database as a excell sheet"""
    return render(request, 'order_list.html',
                      {#'data': {**FormUser.Meta.name2field, 
                       #         **FormOrderItem.Meta.name2field},
                       # 'data' : list(FormUser.Meta.name2field.values()) + list(FormOrderItem.Meta.name2field.values()),
                        'data' : get_list(),
                        'order' : get_rows_in_str()})

#def delete(request, oid):
#    try:
#        ord = get_object_or_404(Order, pk=oid)
#    except ObjectDoesNotExist as dne:
#        return render(request, "<h2>Order doesn't exist</h2>")
#    if request.method == 'POST':
#        ord.delete()
#        return render(request, "order_app:list")
#    return render(request, 'delete.html', {'orders':ord})

def adding_data(request):
    """Reading csv files, join together all information 
       and keep data in the database"""
    path = 'mvc_demo/data csv'
    data2data = {
                'Order ID'  :  'id_n',
                'Order Date'  :   'order_data',
                'CustomerName' : 'first_name',
                'State' : 'country',
                'City'  : 'city',
                'Amount' : 'price',
                'Profit' :  '',
                'Quantity' : 'quantity',
                'Category' : '', #'description',
                'Sub-Category' : 'description',
                'Month of Order Date' : '',
                'Target' : ''
                }
    data = {}
    data_fram_1 = pd.read_csv(f"{path}/User.csv")
    data_fram_2 = pd.read_csv(f"{path}/Order.csv")
    forms = []
    ind_1 = 0
    for order_id_1 in data_fram_1['Order ID']:
        ind_2 = 0
        for order_id_2 in data_fram_2['Order ID']:
            new_data = {}
            if order_id_1 == order_id_2:
                for key in data_fram_1:
                    new_data[key] = data_fram_1[key][ind_1]
                for key in data_fram_2:
                    new_data[key] = data_fram_2[key][ind_2]
                forms.append(new_data)
            ind_2 += 1
        ind_1 += 1
    translated_forms = [{data2data[key]: val for key, val in data.items()
                         if data2data[key]} 
                         for data in forms]
    tmp = {'email' : 'example@example.com', 'surname' :'Nan',
           'phone_number' : 123456789, 'street' : 'Nan' }
    for data in translated_forms:
        data.update(tmp)
        add_data(data)
    return HttpResponse("<h1>Data are filled</h1>")
    #with open(file_, 'r') as f_obj:
    #    reader = csv.reader(f_obj)
    #    for row in reader:
    #        print(row)
    #        breakpoint()
    #data_frame = pd.read_csv(file_)
    #data.update({ key_: []  for key_ in data_frame})
    #for key_ in data_frame:
    #    data[key_] = list(data_frame[key_])
    #for key, _ in data.items():
    #    print(key)
    #print(list(data.keys()))