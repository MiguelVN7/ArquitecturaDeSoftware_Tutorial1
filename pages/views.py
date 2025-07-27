from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

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

# Product class
class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price":"$1500"},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price":"$1000"},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price":"$100"},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price":"$250"}
    ]

# Product Index Page
class ProductIndexView(TemplateView):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of Products"
        viewData["products"] = Product.products

        return render(request, self.template_name, viewData)

# Product Show Page
class ProductShowView(TemplateView):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        try:
            product = Product.products[int(id) - 1]

            viewData["title"] = product["name"] + "- Online Store"
            viewData["subtitle"] = product["name"] + "- Product Information"
            viewData["product"] = product
            price_str = product["price"].replace("$", "") 
            product["price_as_int"] = int(price_str)

            return render(request, self.template_name, viewData)
        except IndexError:
            return HttpResponseRedirect(reverse('home'))
            
# Product Form class
class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
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
            return redirect('new_product')
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)
        
class NewProductCreatedView(TemplateView):
    template_name = 'products/product_created.html'
