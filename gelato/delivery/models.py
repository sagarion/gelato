# -*- coding: utf-8 -*-
from django.db import models
from photo.models import Justification

class IceCream(models.Model):
    name = models.CharField(max_length=100, unique=True)
    barcode = models.CharField(max_length=20, unique=True)

    class meta :
        verbose_name = "iceCream"
        verbose_name_plural = "iceCreams"



class User(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Delivery(models.Model):
    creation = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User)
    deliveryLines = models.ManyToManyField(IceCream, through='DeliveryLine')
    justification = models.ForeignKey(Justification, null=True)


    def __str__(self):
        return 'Livraison ' + self.id + ', par' + self.user.name + ", le" + self.creation

    def add_iceCream(self, iceCream, quantity):
        request = DeliveryLine.objects.filter(delivery= self, iceCream= iceCream.id)
        if request.count() == 1:
            line = request.first()
            line.quantity = line.quantity + quantity
            line.save()
        else:
            line = DeliveryLine.objects.create(delivery=self, iceCream=iceCream, quantity=quantity)
            line.save()

    def delete_deliveryLine(self, deliveryLine):
        # vérifie que la ligne de livraison appartient bien à la livraison
        if deliveryLine.delivery.id == self.id:
            deliveryLine.delete()
            self.save()
        else:
            raise ValueError('Apparamment la ligne de livraison supprimé n\'appartient pas à la livraison ...')


    def substract_iceCream(self, iceCream, quantity):
        request = DeliveryLine.objects.filter(delivery=self, iceCream=iceCream.id)
        if request.count()== 1:
            line = request.first()
            if line.quantity <= quantity:
                self.delete_deliveryLine(line.id)
            else:
                line.quantity = line.quantity - quantity
                line.save()
        else:
            raise ValueError('Apparamment la commande ne possède pas ce type de glace')


class DeliveryLine(models.Model):
    delivery = models.ForeignKey(Delivery)
    iceCream = models.ForeignKey(IceCream)
    quantity = models.IntegerField()


