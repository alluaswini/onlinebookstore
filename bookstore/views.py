
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Cart, CartItem, Order
from .forms import OrderForm

def book_search(request):
    if request.method == 'GET':
        query = request.GET.get('search')
        books = Book.objects.filter(title__icontains=query)
        return render(request, 'results.html', {'books': books})

def book_detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        cart = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.create(cart=cart, book=book)
        return redirect('cart')
    return render(request, 'detail.html', {'book': book})

def cart(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)
    cart_total = sum([item.book.price for item in cart_items])
    return render(request, 'cart.html', {'cart_items': cart_items, 'cart_total': cart_total})

def checkout(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            cart_items = CartItem.objects.filter(cart__user=request.user)
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                total=sum([item.book.price for item in cart_items])
            )
            cart_items.delete()
            return redirect('order_confirmation')
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'form': form})

def order_confirmation(request):
    return render(request, 'order_confirmation.html')
