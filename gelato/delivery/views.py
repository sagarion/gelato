from delivery.models import User, Delivery, IceCream, DeliveryLine
from photo.models import Justification
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'delivery/index.html', context)


def user_new(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('user_details', user_id=user.id)
    else:
        form = UserForm()
    return render(request, 'delivery/user_create.html', {'form': form})


def user_details(request, user_id):
    template = loader.get_template('delivery/user_details.html')
    deliveries = Delivery.objects.filter(user_id=user_id)
    user = User.objects.get(id=user_id)
    context = {'user': user,
               'deliveries': deliveries,
               }
    return HttpResponse(template.render(context, request))

    #test recuperation user.name
    #return HttpResponse("<h1> liste livraison de " + user.name + "</h1>")

    # test recuperation inventories
    #return HttpResponse("<h1> liste livraison de " + str(inventories.first().date) + "</h1>")


def iceCream_new(request):
    if request.method == "POST":
        form = IceCreamForm(request.POST)
        if form.is_valid():
            iceCream = form.save(commit=False)
            iceCream.save()
            return redirect('iceCream_details', id=iceCream.id)
    else:
        form = IceCreamForm()
    return render(request, 'delivery/iceCream_create.html', {'form': form})


def iceCream_detail(request, id):
    iceCream = get_object_or_404(IceCream, id=id)
    return render(request, 'delivery/iceCream_details.html', {'iceCream': iceCream})


def delivery_create(request, user_id):

            delivery = Delivery()
            delivery.user_id = user_id
            delivery.save()
            return redirect('delivery_inventory', delivery_id=delivery.id)

def delivery_new(request):
    if request.method == "POST":
        form = DeliveryForm(request.POST)
        if form.is_valid():

            delivery = form.save(commit=False)
            delivery.save()
            return redirect('delivery_details', id=delivery.id)
    else:
        form = UserForm()
    return render(request, 'delivery/delivery_create.html', {'form': form})

def delivery_inventory(request, delivery_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    iceCreams = IceCream.objects.all()
    inventory = DeliveryLine.objects.filter(delivery=delivery)
    if request.method == "POST":
        form = Delivery_select_iceCreamForm(request.POST)
        if form.is_valid():
            barcodeForm = form.cleaned_data['barcode']
            iceCream = IceCream.objects.filter(barcode=barcodeForm)
            if iceCream.count() == 1:
                return redirect('delivery_iceCream_add', delivery_id=delivery.id, iceCream_id=iceCream.first().id)
            else:
                iceCream = IceCream()
                iceCream.barcode = form.cleaned_data['barcode']
                iceCream.name = "TEMP"
                iceCream.save()
                iceCream.name = "Unknow " + str(iceCream.id)
                iceCream.save()
                return redirect('delivery_iceCream_add', delivery_id=delivery.id, iceCream_id=iceCream.id)

    else:
        form = Delivery_select_iceCreamForm()
        return render(request, 'delivery/delivery_inventory.html', {'delivery': delivery, 'iceCreams': iceCreams,
                                                                    'form': form, 'inventory': inventory})


def delivery_iceCream_add(request, delivery_id, iceCream_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    iceCream = get_object_or_404(IceCream, id=iceCream_id)

    if request.method == 'POST':
        form = Delivery_quantity_iceCreamForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            delivery.add_iceCream(iceCream, quantity)
            return redirect('delivery_inventory', delivery_id=delivery.id)

    else:
        form = Delivery_quantity_iceCreamForm()
        context = {'delivery': delivery, 'iceCream': iceCream, 'form': form}
        return render(request, 'delivery/delivery_iceCream_add.html', context)

@csrf_exempt
def delivery_iceCream_add_one(request, delivery_id, iceCream_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    iceCream = get_object_or_404(IceCream, id=iceCream_id)
    delivery.add_iceCream(iceCream, 1)
    line = DeliveryLine.objects.filter(delivery=delivery, iceCream=iceCream).first()

    return JsonResponse({'id': line.id,
                         'product': line.iceCream.name,
                         'quantity':line.quantity,
                         'barcode': line.iceCream.barcode})

def delivery_deliveryLine_delete(request, delivery_id, deliveryLine_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    delivery_line = get_object_or_404(DeliveryLine, id=deliveryLine_id)
    delivery.delete_deliveryLine(delivery_line)
    return redirect('delivery_inventory', delivery_id=delivery.id)

def delivery_delete_line(request, delivery_id, line_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    line = get_object_or_404(DeliveryLine, id=line_id)
    line.delete()
    return redirect('delivery_inventory', delivery_id=delivery.id)

@csrf_exempt
def delivery_iceCream_substract_one(request, delivery_id, iceCream_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    iceCream = get_object_or_404(IceCream, id=iceCream_id)
    delivery.substract_iceCream(iceCream, 1)
    line = DeliveryLine.objects.filter(delivery=delivery, iceCream=iceCream).first()

    return JsonResponse({'id': line.id,
                         'product': line.iceCream.name,
                         'quantity': line.quantity,
                         'barcode': line.iceCream.barcode})

def delivery_delete_delivery(request, delivery_id, user_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    delivery.delete()
    return redirect('user_details', user_id=user_id)

