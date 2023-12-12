from django.shortcuts import render,redirect
from django.http import HttpResponse
from myapp.models import Product,Cart,Buy,Review,Category
from myapp.forms import CartForm,ReviewForm
from myapp.myapp import *
from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


# Create your views here.

def category(request):
    c= Category.objects.all()
    context={'c':c}
    print(c)
    return render(request,'categories.html',context)

def products(request,product_id,slug):
    p=Product.objects.filter(category=product_id)
    if request.GET.get('q'):
        query=request.GET.get('q')
        p=Product.objects.filter(title__contains=query)
    context={'p':p}
    return render(request,'index.html',context)
    
def detail(request,product_id,slug):
    d=Product.objects.get(id=product_id)
    if request.method=="POST":
        f=CartForm(request,request.POST)
        if f.is_valid():
            request.form_data=f.cleaned_data
            add_to_cart(request)
            return redirect('myapp:cart_view')
    f=CartForm(request,initial={'product_id':product_id})
    context={'d':d,'f':f}
    return render(request,'detail.html',context)
def cart_view(request):
    if request.method=="POST" and request.POST.get('delete')=='Delete':
        item_id=request.POST.get('item_id')
        cd=Cart.objects.get(id=item_id)
        cd.delete( )
    c=get_cart(request)
    t=total_(request)
    co=item_count(request)
    context={'c':c,'t':t}
    return render(request,'cart.html',context)
def order(request):
    # What you want the button to do.
    items=get_cart(request)
    for i in items:
        b=Buy(product_id=i.product_id,quantity=i.quantity,price=i.price)
        b.save()
    paypal_dict = {
        "business": "sb-l7r2e28145955@business.example.com",
        "amount": total_(request),
        "item_name":cart_id(request),
        "invoice": str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('myapp:return_view')),
        "cancel_return": request.build_absolute_uri(reverse('myapp:cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form,"items":items,"total":total_(request)}
    return render(request, "order.html", context)
def return_view(request):
    return HttpResponse('Transaction Succesful')
def cancel_view(request):
    return HttpResponse('Transaction Cancelled')
def grocery(request):
    return render(request,'grocery.html')
def review(request,product_id,slug):
    d=Product.objects.get(id=product_id)
    reviews = Review.objects.filter(post_id = product_id)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.cleaned_data['review']
            c = Review(post_id = product_id,review = review,user = request.user)
            c.save()
            
    else:
        form = ReviewForm()

    return render(request, 'review.html', {'d':d,'form': form,'reviews':reviews})    


def send_email(request):
    subject = request.POST.get("subject", "Hi codegnan")
    message = request.POST.get("message", "otp is 218404")
    from_email = request.POST.get("from_email", "bobbadichaitanya3@gmail.com")
    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, ["tksiva05@gmail.com"])
        except BadHeaderError:
            return HttpResponse("Invalid header found.")
        return HttpResponseRedirect("Mail sent to pk")
    else:
        # In reality we'd use a form class
        # to get proper validation errors.
        return HttpResponse("Make sure all fields are entered and valid.")