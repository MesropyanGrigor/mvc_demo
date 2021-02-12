from django.shortcuts import render, get_object_or_404
from .forms import FormUser, FormOrder, FormOrderItem
from .models import User, Order, OrderItem
from django.http import HttpResponse
from django.contrib import messages
from django.core.exceptions import  ObjectDoesNotExist

# Create your views here.


def order(request):
    if request.method == 'POST':
        user_form = FormUser(request.POST)
        order_form = FormOrder(request.POST)
        orderitem_form = FormOrderItem(request.POST) 
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
        #messages.success(request, "Order is successfully added", extra_tags='alert')
        return HttpResponse("<h1>Order is submitted</h1>")
    else:
        return render(request, 'order.html',
                      {'data': {**FormUser.Meta.name2field, 
                                **FormOrderItem.Meta.name2field}})


def get_rows_in_str():
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
    new_dict = dict([(value, key) for key, value in dict_0.items()])  # swaping dict
    return  [new_dict[field] for field in 
             FormOrderItem.Meta.fields +  FormOrder.Meta.fields + FormUser.Meta.fields]

def ordered(request=None):
    return render(request, 'data.html', {'rows' : get_rows_in_str})


def temp(request):
    print(get_list())
    return render(request, 'order_list.html',
                      {#'data': {**FormUser.Meta.name2field, 
                       #         **FormOrderItem.Meta.name2field},
                       # 'data' : list(FormUser.Meta.name2field.values()) + list(FormOrderItem.Meta.name2field.values()),
                        'data' : get_list(),
                        'order' : get_rows_in_str()})

def update(request):
    return render(request, 'update.html', {})


def delete(request, oid):
    #breakpoint()
    try:
        ord = get_object_or_404(Order, pk=oid)
    except ObjectDoesNotExist as dne:
        return render(request, "<h2>Order doesn't exist</h2>")
    if request.method == 'POST':
        ord.delete()
        return render(request, "order_app:list")
    return render(request, 'delete.html', {'orders':ord})


def adding_data():
    import glob
    path = 'mvc_demo/data csv'
    import pandas as pd
    data = {}
    for file_ in glob.glob(f"{path}/*csv"):
        print(file_)
        #with open(file_, 'r') as f_obj:
        #    reader = csv.reader(f_obj)
        #    for row in reader:
        #        print(row)
        #        breakpoint()
        data_frame = pd.read_csv(file_)
        data.update({ key_: []  for key_ in data_frame})

        for key_ in data_frame:
            data[key_] = list(data_frame[key_])
    print(list(data.keys()))
    breakpoint()

adding_data() 