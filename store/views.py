from django.shortcuts import render
from django.db.models import DecimalField ,F,Func,ExpressionWrapper, Count, Avg, Max, Value
# from django.http import HttpR response

from .models import  Product, OrderItem, Order, Customer, Comment

def show_data(request):
    # q = Product.objects.filter(inventory__in=(80, 91))
    # q = Product.objects.prefetch_related('product')
    # q = Product.objects.prefetch_related('order_items').all()
    #q = Product.objects.prefetch_related('comments').select_related('category').all()
    
    # q = Product.objects.order_by('-unit_price')
    # q = Product.objects.order_by('-inventory').values('name', 'inventory')
    # q = Product.objects.filter(inventory__gt=10).aggregate(count=Count('id'),
    #                                                       avg=Avg('inventory'))
    # q = Product.objects.annotate(x=Value("😊")).all()[:2]
    # q = Customer.objects.annotate(full_name=Func(F('first_name'), 
    #                                              Value(' '),
    #                                              F('last_name'), 
    #                                              function='CONCAT'))
    # q = OrderItem.objects \
    #              .values('order_id') \
    #              .annotate(count=Count('order_id'))
    # q = Customer.objects.annotate(customer_count=Count('orders'))
    q = OrderItem.objects.annotate(total_price=ExpressionWrapper(F('quantity')*F('unit_price'), output_field=DecimalField()))
                         
    print(q)
    return render(request, 'hello.html')#, {'products': list(q)})

def show_comment(request):
    q = Comment.approved.select_related('product').all()
    # q = Comment.objects.all()
    
    return render(request, 'comment.html', {'comments': list(q)})

def show_oderitem(request):
    # q = Product.objects.filter(id__in=OrderItem.objects.values("product_id").distinct())
    # q = OrderItem.objects.filter(product__id__in=range(1000, 2000,1))
    # q = OrderItem.objects.select_related('product').all()
    q = Order.objects.prefetch_related('items__product').select_related('customer')
    return render(request, 'orderitem.html', {'oderitems': list(q)})

def show_product_with5inventory(request):
    # q = Product.objects.filter(~Q(inventory__lt=5) |  Q(inventory__gt=95))
    q = Product.objects.filter(inventory=5)[:3]
    # q = Product.objects.filter(name__icontains='site', inventory__gt=3)
    # q = Product.objects.filter(name__icontains='site', inventory__gt=3, inventory__lt=50)
    # q = Order.objects.filter(status=Order.ORDER_STATUS_UNPAID)
    # q = Order.objects.exclude(status=Order.ORDER_STATUS_UNPAID)
    # q = OrderItem.objects.filter(order_id=1)
    # q = Product.objects.filter(unit_price__lt=10)
    # q = Customer.objects.filter(first_name__icontains='john')
    # q = Order.objects.filter(customer__in=q)
    
    return render(request, 'inventory.html', {'products': list(q)})