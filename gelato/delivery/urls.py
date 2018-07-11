from django.conf.urls import url
from . import views

urlpatterns = [
    #index
    #/delivery/
    url(r'^$', views.index, name='index'),

    # /delivery/user/new/
    url(r'^user/new/$', views.user_new, name='user_create'),

    # /delivery/user/756
    url(r'^user/(?P<user_id>\d+)/$', views.user_details, name='user_details'),

    #/delivery/delivery/new/756
    url(r'^delivery/new/(?P<user_id>\d+)/$', views.delivery_create, name='delivery_create'),


    #/delivery/iceCream/new/
    url(r'^iceCream/new/$', views.iceCream_new, name='iceCream_create'),

    #/delivery/iceCream/756
    url(r'^iceCream/(?P<id>\d+)/$', views.iceCream_detail, name='iceCream_details'),

    # access to an inventory (manipulation)
    # /delivery/delivery/756
    url(r'^delivery/(?P<delivery_id>\d+)/$', views.delivery_inventory, name='delivery_inventory'),

    # add several iceCreams to a delivery
    #/delivery/delivery/756/iceCream/756/add/
    url(r'^delivery/(?P<delivery_id>\d+)/iceCream/(?P<iceCream_id>\d+)/add/$', views.delivery_iceCream_add,
        name='delivery_iceCream_add'),

    # add one iceCream to a delivery
    #/delivery/delivery/756/iceCream/756/addone/
    url(r'^delivery/(?P<delivery_id>\d+)/iceCream/(?P<iceCream_id>\d+)/addOne/$', views.delivery_iceCream_add_one,
        name='delivery_iceCream_addone'),

    # delete a delivery line from a delivery
    # /delivery/delivery/756/line/756/delete/
    url(r'^delivery/(?P<delivery_id>\d+)/line/(?P<deliveryLine_id>\d+)/delete/$', views.delivery_deliveryLine_delete,
        name='delivery_line_delete'),

    # substract an iceCream from a delivery
    # /delivery/delivery/756/line/756/delete/
    url(r'^delivery/(?P<delivery_id>\d+)/iceCream/(?P<iceCream_id>\d+)/substractOne/$',
        views.delivery_iceCream_substract_one, name='delivery_line_substractone'),

    # delete a delivery
    # /delivery/delete/756/user/756/
    url(r'^delete/(?P<delivery_id>\d+)/user/(?P<user_id>\d+)/$',
        views.delivery_delete_delivery, name='delivery_delete'),
]