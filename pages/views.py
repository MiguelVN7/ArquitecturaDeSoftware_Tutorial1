from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Home Page
class HomePageView(TemplateView):
    template_name = 'pages/home.html'

# About Page
class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    # Get the information about us
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Miguel Villegas N",
        })
        return context

# Contact Page  
class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    # Get the information for contacting us
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact - Online Store",
            "subtitle": "You can contact us with the following: ",
            "description": "mvillegas7@gmail.com - 310 789 1278",
            "author": "Miguel Villegas N",
        })
        return context


# Product Index Page
class ProductIndexView(TemplateView):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of Products"
        viewData["products"] = Product.objects.all()

        return render(request, self.template_name, viewData)

# Product Show Page
class ProductShowView(TemplateView):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError('Product id must me 1 or greater')
            product = get_object_or_404(Product, pk=product_id)
        except(ValueError, IndexError):
            return HttpResponseRedirect(reverse('home'))
        
        viewData = {}
        product = get_object_or_404(Product, pk=product_id)
        viewData['title'] = product.name + ' - Online Store'
        viewData['subtitle'] = product.name + ' - Product Information'
        viewData['product'] = product

        return render(request, self.template_name, viewData)
            
# Product Form class
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price

# Product Create Page
class ProductCreateView(TemplateView):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)
    
    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('new_product', product_id=product.id)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of Products'
        return context
        
class NewProductCreatedView(TemplateView):
    template_name = 'products/product_created.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            context['product'] = product
            context['title'] = 'Product Created'
            context['success'] = True
        except Product.DoesNotExist:
            context['success'] = False
        return context
